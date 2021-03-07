<script context="module">
    export async function preload(page, session) {
        let slug = "http://api:5000/utils/states";
        if (!session.posts.hasOwnProperty(slug)) {
            let aux = await this.fetch(slug);
            session.posts[slug] = await aux.json();
        }
        const estados = session.posts[slug];

        slug = "http://api:5000/utils/genres";
        if (!session.posts.hasOwnProperty(slug)) {
            let aux = await this.fetch(slug);
            session.posts[slug] = await aux.json();
        }
        const generos = session.posts[slug];

        slug = "http://api:5000/book/";
        if (!session.posts.hasOwnProperty(slug)) {
            let aux = await this.fetch(slug);
            session.posts[slug] = await aux.json();
        }
        const books = session.posts[slug];

        return { books, estados, generos };
    }
</script>

<!-- src/routes/cadastro/_layout.svelte -->
<script>
    import { onMount } from "svelte";

    var searchInputDropdownCliente, dropdownMenuCliente;

    onMount(async () => {
        document.querySelectorAll(".form-outline").forEach((formOutline) => {
            if (typeof mdb != "undefined") new mdb.Input(formOutline).init();
        });
        searchInputDropdownCliente = document.querySelector("#inputSearchCostumer");
        VMasker(searchInputDropdownCliente).maskPattern("999.999.999-99");
        dropdownMenuCliente = searchInputDropdownCliente.parentNode.querySelector(".dropdown-menu");
        document.querySelector("#form_new_order").addEventListener("submit", formSubmit);

        let slug = "http://localhost:5000/book/";
        let aux = await fetch(slug);
        books = await aux.json();
    });

    const formSubmit = (e) => {
        e.preventDefault();

        // get form
        var formdata = new FormData(e.target);

        // trim the values
        var keys_trimmed = [];
        for (let key of formdata.keys()) {
            if (keys_trimmed.indexOf(key) != -1) continue;
            if (key.includes("[]") && key.indexOf("[]") == key.length - 2) {
                let values = formdata.getAll(key);
                formdata.delete(key);
                for (let v of values) {
                    formdata.append(key, v.trim());
                }
                console.log(key, formdata.getAll(key));
            } else {
                console.log(key, formdata.get(key).trim());
                formdata.set(key, formdata.get(key).trim());
            }
            keys_trimmed.push(key);
        }

        // validation
        var error, error_message;
        [error, error_message] = window.formSubmitOrder(e);

        // show toast
        document.querySelector("#toast-container") && document.querySelector("#toast-container").remove();

        if (error) {
            var alert_msg = "";
            error_message.map((obj) => {
                if (alert_msg.length > 0) {
                    alert_msg += "<br>";
                }
                alert_msg += obj.message;
            });

            if (!document.querySelector("#toast-container .toast-message")) {
                toastr.error(alert_msg, "Atenção!", {
                    closeButton: true,
                    tapToDismiss: true,
                    preventDuplicates: true,
                });
            } else {
                document.querySelector("#toast-container .toast-message").innerHTML = alert_msg;
            }
        } else {
            var spinner = e.target.querySelector("button[type='submit'] span.spinner");
            if (spinner) spinner.style.display = "inline-block";
            var btn_save_text = document.querySelector("#btn_save_text");
            var bkp_btn_save_text;
            if (btn_save_text) {
                bkp_btn_save_text = btn_save_text.textContent;
                btn_save_text.textContent = "Salvando...";
                btn_save_text.disabled = true;
            }

            let products = formdata.getAll("id_product[]");
            let quantities = formdata.getAll("quantity[]");

            var array_products = [];
            for (let index = 0; index < products.length; index++) {
                let product = { id_product: products[index], quantity: quantities[index] };
                array_products.push(product);
            }

            var json_data = { id_costumer: formdata.get("id_costumer"), products: array_products };

            fetch(`http://localhost:5000/sale/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    mode: "no-cors",
                },
                body: JSON.stringify(json_data),
            })
                .then((response) => {
                    spinner && (spinner.style.display = "none");
                    btn_save_text && (btn_save_text.textContent = bkp_btn_save_text) && (btn_save_text.disabled = false);

                    if (response.ok) {
                        var contentType = response.headers.get("content-type");
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            return response.json().then((json) => {
                                if (Object.keys(json).includes("id")) {
                                    toastr.info("Venda realizada com sucesso!", "Tudo certo!", {
                                        closeButton: true,
                                        tapToDismiss: true,
                                        preventDuplicates: true,
                                    }) && document.querySelector("#form_new_order").reset();
                                    costumer = [];
                                    books_added = [];
                                    document.querySelector("#inputSearchCostumer").value = "";
                                } else {
                                    Object.keys(json).includes("error") &&
                                        toastr.error(json.error, "Atenção!", {
                                            closeButton: true,
                                            tapToDismiss: true,
                                            preventDuplicates: true,
                                        });
                                    console.log(json);
                                }
                            });
                        } else {
                            console.log("Oops, we haven't got JSON!");
                            response.text().then((response) => {
                                console.log(response);
                            });
                        }
                    } else {
                        console.error("Network response was not ok.");
                    }
                })
                .catch((error) => {
                    spinner && (spinner.style.display = "none");
                    btn_save_text && (btn_save_text.textContent = bkp_btn_save_text) && (btn_save_text.disabled = false);

                    console.error("There has been a problem with your fetch operation: " + error.message);
                });
        }
    };

    const hiddenList = () => {
        setTimeout(() => {
            dropdownMenuCliente.style.display = "none";
        }, 500);
    };

    const updateList = async (e) => {
        var filter = searchInputDropdownCliente.value.toLowerCase();
        filter = filter.trim().replace(/\.|-|'/g, "");

        if (filter) {
            let endpoint = `http://localhost:5000/costumer/?field=cpf&val=${filter}`;
            dropdownMenuCliente.querySelectorAll(".dropdown-item").forEach((el) => {
                el.style.display = "none";
            });
            dropdownMenuCliente.style.display = "block";
            if (!(endpoint in window._cache_)) {
                // check if this search is a subset of another already cached
                var keys = Object.keys(window._cache_).filter((k) => {
                    if (endpoint.startsWith(k) && k.length < endpoint.length) {
                        return k;
                    }
                });

                let cachedEndpoint;
                if (!!keys.length) {
                    keys.sort().reverse();
                    cachedEndpoint = keys[0];
                }

                if (cachedEndpoint) {
                    costumers = window._cache_[cachedEndpoint];
                } else {
                    var spinner = dropdownMenuCliente.querySelector(".spinner");
                    spinner.style.display = "block";
                    let res = await fetch(endpoint);
                    costumers = await res.json();
                    spinner.style.display = "none";
                    window._cache_[endpoint] = costumers;
                }
            } else {
                costumers = window._cache_[endpoint];
            }
            setTimeout(() => {
                dropdownMenuCliente.querySelectorAll(".dropdown-item").forEach((el) => {
                    el.style.display = "flex";
                });

                const valueExist = !!filter.length;

                if (valueExist) {
                    let existsResults = false;
                    dropdownMenuCliente.querySelectorAll(".dropdown-item").forEach((el) => {
                        const elText = el.getAttribute("cpf").trim().toLowerCase();
                        const isIncluded = elText.includes(filter);
                        if (!isIncluded) {
                            el.style.display = "none";
                        } else {
                            existsResults = true;
                        }
                    });
                    !existsResults && (dropdownMenuCliente.style.display = "none");
                }
            }, 100);
        } else {
            dropdownMenuCliente.style.display = "none";
        }
    };

    const fillInfoCostumer = (e) => {
        e.preventDefault();
        costumers.map((pessoa) => {
            if (e.target.getAttribute("cpf") == pessoa.cpf) {
                costumer = pessoa;

                // format cpf
                costumer.cpf = costumer.cpf.replace(/[^\d]/g, "").replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");

                // format data_nascimento
                costumer.birth_date = costumer.birth_date.split("-").reverse().join("/");
            }
        });
        dropdownMenuCliente.style.display = "none";
    };

    const addNewBook = (e) => {
        const select_books = document.querySelector("#select_books");
        const id_book = select_books.options[select_books.selectedIndex].value;

        for (let book of books) {
            if (book.id == id_book) {
                let obj_copy = Object.assign({}, book);
                obj_copy.key = Math.random();
                obj_copy.unit_chosen = 1;
                books_added = books_added.concat(obj_copy);
                break;
            }
        }
    };

    const removeNewBook = (e) => {
        let obj = e.target;
        obj.tagName == "I" && (obj = obj.parentNode);
        const key = obj.dataset.key;

        books_added = books_added.filter((b) => b.key != key);
    };

    let books_added = [];
    let costumer = [];
    let costumers = [];
    export let books;
    export let segment;
    export let generos;
    export let estados;
</script>

<svelte:head>
    <title>Venda de Livros</title>
</svelte:head>

<h1>Realizar Nova Venda</h1>

<div class="mt-4">
    <div class="form-outline float-start">
        <input
            type="text"
            class="form-control"
            id="inputSearchCostumer"
            placeholder="999.999.999-99"
            maxlength="14"
            onkeydown="return onlyNumbers(event);"
            on:keyup={updateList}
            on:blur={hiddenList}
        />
        <label for="inputSearchCostumer" class="form-label">Buscar Cliente</label>

        <ul class="dropdown-menu">
            <div class="spinner">
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
            </div>
            {#each costumers as costumer}
                <li>
                    <a class="dropdown-item" cpf={costumer.cpf} href="#list" on:click={fillInfoCostumer}>{costumer.full_name}</a>
                </li>
            {/each}
        </ul>
    </div>
</div>

<div class="clear">
    <form class="row g-3" id="form_new_order">
        <div class="col-md-12">
            <fieldset class="border p-2">
                <legend class="w-auto fieldset-title">Dados do Cliente</legend>

                {#if !!costumer.id}
                    <input type="hidden" value={costumer.id} name="id_costumer" />
                    <div class="d-flex">
                        <div class="title col-md-3">Nome:</div>
                        <div class="desc col-md-9">{costumer.full_name}</div>
                    </div>
                    <div class="d-flex">
                        <div class="title col-md-3">CPF:</div>
                        <div class="desc col-md-9">{costumer.cpf}</div>
                    </div>
                    <div class="d-flex">
                        <div class="title col-md-3">Data de Nascimento:</div>
                        <div class="desc col-md-9">{costumer.birth_date}</div>
                    </div>
                    <div class="d-flex">
                        <div class="title col-md-3">Número de Contato:</div>
                        <div class="desc col-md-9">{costumer.phone}</div>
                    </div>
                    <div class="d-flex">
                        <div class="title col-md-3">Email:</div>
                        <div class="desc col-md-9">{costumer.email}</div>
                    </div>
                    <div class="d-flex">
                        <div class="title col-md-3">Endereço:</div>
                        <div class="desc col-md-9">{costumer.address}</div>
                    </div>
                    {#if costumer.complement}
                        <div class="d-flex">
                            <div class="title col-md-3">Complemento:</div>
                            <div class="desc col-md-9">{costumer.complement}</div>
                        </div>
                    {/if}
                {:else}
                    <div class="advice">Selecione o cliente.</div>
                {/if}
            </fieldset>
        </div>

        <div class="col-md-12">
            <fieldset class="border p-2 d-flex justify-content-center flex-column">
                <legend class="w-auto fieldset-title">Adicione os Livros</legend>

                <div class="d-flex justify-content-center align-items-center">
                    <div class="select-input select-livro">
                        <select class="form-select" id="select_books">
                            <option value="0" selected>-</option>
                            {#if books && books.length > 0}
                                {#each books as book}
                                    <option value={book.id}>{book.title}</option>
                                {/each}
                            {/if}
                        </select>
                    </div>
                    <button type="button" class="btn btn-primary btn-sm ms-3" on:click={addNewBook}>Add New</button>
                </div>

                <div class="d-flex justify-content-center flex-column mt-3">
                    {#if books_added && books_added.length > 0}
                        <table class="table table-light table-hover table-responsive-sm align-middle">
                            <caption style="caption-side:top">Livros Adicionados</caption>
                            <thead>
                                <tr>
                                    <th class="th-9 border text-center col-6">Title</th>
                                    <th class="th-9 border text-center col-2">Unit Price</th>
                                    <th class="th-9 border text-center col-2">Quantity</th>
                                    <th class="th-9 border text-center col-2">Sum</th>
                                    <th class="th-6 border text-center col-2">Action</th>
                                </tr>
                            </thead>

                            {#each books_added as book}
                                <tbody>
                                    <tr>
                                        <td class="border text-center">{book.title}</td>
                                        <td class="border text-center">${book.price.toFixed(2)}</td>
                                        <td class="border text-center">
                                            <input type="hidden" name="id_product[]" value={book.id} />
                                            <input type="number" min="1" name="quantity[]" value="1" on:change={(e) => (book.unit_chosen = e.target.value)} />
                                        </td>
                                        <td class="border text-center">${(book.price * book.unit_chosen).toFixed(2)}</td>
                                        <td class="border text-center">
                                            <button type="button" title="Remove" data-key={book.key} on:click={removeNewBook}>
                                                <i class="fa fa-times red-text btn_remove_book" disabled />
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            {/each}
                        </table>

                        <div class="d-flex flex-column justify-content-center align-items-center">
                            <div>
                                <span class="fw-bold">Total Sum:</span> ${books_added
                                    .reduce((acc, curr) => {
                                        return acc + curr.price * curr.unit_chosen;
                                    }, 0)
                                    .toFixed(2)}
                            </div>
                            {#if !!costumer.id}
                                <div>
                                    <span class="fw-bold">Customer discount:</span>
                                    {costumer.discount}%
                                </div>
                                <div>
                                    <span class="fw-bold">Total Purchase:</span> ${(
                                        books_added.reduce((acc, curr) => {
                                            return acc + curr.price * curr.unit_chosen;
                                        }, 0) -
                                        (books_added.reduce((acc, curr) => {
                                            return acc + curr.price * curr.unit_chosen;
                                        }, 0) *
                                            costumer.discount) /
                                            100
                                    ).toFixed(2)}
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            </fieldset>
        </div>

        {#if !!costumer.id}
            <div class="col-12">
                <button type="submit" class="btn btn-primary float-end"
                    ><span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true" style="display:none" />
                    <span id="btn_save_text">Realizar a Venda</span>
                </button>
            </div>
            <script>
                document.querySelectorAll(".form-outline").forEach((formOutline) => {
                    typeof mdb != "undefined" && new mdb.Input(formOutline).init();
                });
            </script>
        {/if}
    </form>
</div>

<style>
    .form-select {
        height: 35px;
        min-width: 150px;
    }
    .form-control:focus,
    .form-select:focus {
        color: #1266f1;
    }
    .select-input {
        position: relative;
        width: 100%;
    }
    .form-outline {
        width: 100%;
    }
    .select-input select {
        border-color: #bbb;
    }
    legend.fieldset-title {
        padding: 0 5px;
        border-bottom: none;
        float: unset;
        font-size: 15px;
    }
    .spinner {
        text-align: center;
        display: none;
    }
    div.clear {
        clear: both;
    }
    .title {
        font-weight: bold;
        text-align: right;
        padding-right: 10px;
        white-space: nowrap;
    }
    .select-livro {
        float: left;
        min-width: 150px;
        margin-top: 20px;
        clear: left;
        width: 100%;
    }
    .select-livro .form-select {
        max-width: 450px;
    }
    fieldset .advice {
        text-align: center;
        color: darkgray;
    }

    #inputSearchCostumer ~ ul.dropdown-menu {
        overflow: auto;
        max-height: 250px;
    }

    form fieldset {
        border-radius: 4px;
    }

    .btn_remove_book {
        color: red;
    }

    @media (min-width: 500px) {
        .select-livro {
            float: left;
            margin-top: 0;
            clear: unset;
            width: auto;
        }
        .select-input,
        .form-outline {
            width: auto;
        }
    }
</style>
