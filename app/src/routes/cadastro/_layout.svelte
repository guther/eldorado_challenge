<script context="module">
    export async function preload(page, session) {
        let slug = "http://api:5000/book/";
        if (!session.posts.hasOwnProperty(slug)) {
            let aux = await this.fetch(slug);
            session.posts[slug] = await aux.json();
        }
        const books = session.posts[slug];
    }
</script>

<!-- src/routes/cadastro/_layout.svelte -->
<script>
    import { onMount } from "svelte";

    onMount(() => {
        document.querySelector("#btn_add_mock").addEventListener("click", addMockDataForm);

        document.querySelector("#form_new_register").addEventListener("submit", formSubmit);
    });

    function addMockDataForm(e) {
        window.addMockDataForm(e);
    }

    function formSubmit(e) {
        e.preventDefault();

        // get form
        var formdata = new FormData(e.target);

        // trim the values
        for (let key of formdata.keys()) {
            formdata.set(key, formdata.get(key).trim());
        }

        // validation
        var error, error_message;
        [error, error_message] = window.formSubmitPessoa(e);

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

            let endpoints = { cliente: "costumer", livro: "book" };

            let json_data = JSON.stringify(Object.fromEntries(formdata));

            fetch(`http://localhost:5000/${endpoints[segment]}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    mode: "no-cors",
                },
                body: json_data,
            })
                .then((response) => {
                    spinner && (spinner.style.display = "none");
                    btn_save_text && (btn_save_text.textContent = bkp_btn_save_text) && (btn_save_text.disabled = false);

                    if (response.ok) {
                        var contentType = response.headers.get("content-type");
                        if (contentType && contentType.indexOf("application/json") !== -1) {
                            return response.json().then((json) => {
                                if (Object.keys(json).includes("id")) {
                                    toastr.info("Cadastro salvo com sucesso!", "Tudo certo!", {
                                        closeButton: true,
                                        tapToDismiss: true,
                                        preventDuplicates: true,
                                    }) && document.querySelector("#form_new_register").reset();
                                } else {
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
                    console.error("There has been a problem with your fetch operation: " + error.message);
                    spinner && (spinner.style.display = "none");
                    btn_save_text && (btn_save_text.textContent = bkp_btn_save_text) && (btn_save_text.disabled = false);
                    toastr.error("Ocorreu um erro durante o processo de cadastro.", "Atenção!", {
                        closeButton: true,
                        tapToDismiss: true,
                        preventDuplicates: true,
                    });
                });
        }
    }

    export let segment;
</script>

<h1>Cadastro de {segment == "livro" ? "Livros" : "Clientes"}</h1>

<form class="row g-3 mt-2" id="form_new_register">
    <input type="hidden" value={segment} name="form" id="type_register" />

    <slot />

    <div class="col-12">
        <button type="submit" class="btn btn-primary"
            ><span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true" style="display:none" />
            <span id="btn_save_text">Salvar</span></button
        >
        <button id="btn_add_mock" type="button" class="btn btn-secondary">Preencher Automaticamente (testes)</button>
    </div>
</form>

<style>
    :global(.form-select) {
        height: 35px;
    }
    :global(.form-control:focus ~ .select-label, .form-select:focus ~ .select-label) {
        color: #1266f1;
    }
    :global(.select-input) {
        position: relative;
    }
    :global(.select-input select) {
        border-color: #bbb;
    }
    :global(.select-label) {
        position: absolute;
        top: -10px;
        left: 10px;
        background: #fff;
        padding: 0px 4px;
        font-size: 13px;
        font-weight: 400;
        z-index: 1;
    }
    .spinner {
        margin-right: 10px;
    }
</style>
