window._cache_ = {}

var onlyNumbers = (e) => {
    return [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "Backspace",
        "Delete",
        "ArrowLeft",
        "ArrowRight",
    ].includes(e.key);
};

var validateCPF = (cpf) => {
    var soma;
    var resto;
    soma = 0;
    if (cpf == "00000000000") return false;

    for (i = 1; i <= 9; i++) soma = soma + parseInt(cpf.substring(i - 1, i)) * (11 - i);
    resto = (soma * 10) % 11;

    if ((resto == 10) || (resto == 11)) resto = 0;
    if (resto != parseInt(cpf.substring(9, 10))) return false;

    soma = 0;
    for (i = 1; i <= 10; i++) soma = soma + parseInt(cpf.substring(i - 1, i)) * (12 - i);
    resto = (soma * 10) % 11;

    if ((resto == 10) || (resto == 11)) resto = 0;
    return resto == parseInt(cpf.substring(10, 11));
}

var validateEmail = (mail) => {
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail);
}

var mockCPF = () => {
    let number_random = (number) => (Math.round(Math.random() * number));
    let create_array = (total, numero) => Array.from(Array(total), () => number_random(numero));
    let mod = (dividendo, divisor) => Math.round(dividendo - (Math.floor(dividendo / divisor) * divisor));
    let total_array = 9;
    let n = 9;
    let [n1, n2, n3, n4, n5, n6, n7, n8, n9] = create_array(total_array, n);

    let d1 = n9 * 2 + n8 * 3 + n7 * 4 + n6 * 5 + n5 * 6 + n4 * 7 + n3 * 8 + n2 * 9 + n1 * 10;
    d1 = 11 - (mod(d1, 11));
    if (d1 >= 10) d1 = 0;

    let d2 = d1 * 2 + n9 * 3 + n8 * 4 + n7 * 5 + n6 * 6 + n5 * 7 + n4 * 8 + n3 * 9 + n2 * 10 + n1 * 11;
    d2 = 11 - (mod(d2, 11));
    if (d2 >= 10) d2 = 0;

    return `${n1}${n2}${n3}${n4}${n5}${n6}${n7}${n8}${n9}${d1}${d2}`;
}

var addMockDataForm = async (e) => {
    var btn = e.target;
    var type_register = document.querySelector("#type_register").value;

    if (type_register == "cliente") {
        let endpoint = `/utils/mock/costumer`;
        let mock_costumer;
        if (!(endpoint in window._cache_) || window._cache_[endpoint].length == 0) {
            btn.disabled = true;
            let res = await fetch(endpoint);
            mock_costumer = await res.json();
            btn.disabled = false;
            window._cache_[endpoint] = mock_costumer;
        } else {
            mock_costumer = window._cache_[endpoint];
        }

        if (mock_costumer.length > 0) {
            var rand_number = Math.floor(Math.random() * mock_costumer.length);
            var data = mock_costumer[rand_number];

            // full_name
            document.querySelector("#inputName").value = data.full_name;
            document.querySelector("#inputName").focus();

            // cpf
            document.querySelector("#inputCPF").value = mockCPF();
            document.querySelector("#inputCPF").focus();
            document.querySelector("#inputCPF").dispatchEvent(new MouseEvent("keyup"));

            // birth_date
            document.querySelector("#inputDataNascimento").value = data.birth_date;

            // gênero
            document.querySelector("#inputSexo").value = data.id_genre;
            document.querySelector("#inputSexo").focus();

            // phone_number
            document.querySelector("#inputTelefone").value = "92992324133";
            document.querySelector("#inputTelefone").focus();
            document
                .querySelector("#inputTelefone")
                .dispatchEvent(new MouseEvent("keyup"));

            // email
            document.querySelector("#inputEmail").value = data.email;
            document.querySelector("#inputEmail").focus();

            // address
            document.querySelector("#inputEndereco").value = data.address;
            document.querySelector("#inputEndereco").focus();

            // complement
            document.querySelector("#inputComplemento").value = data.complement;
            document.querySelector("#inputComplemento").focus();

            // estado
            document.querySelector("#inputEstado").options[
                Math.floor(
                    Math.random() *
                    (document.querySelector("#inputEstado").options.length - 1)
                ) + 1].selected = true;
            document.querySelector("#inputEstado").focus()
            document.querySelector("#inputEstado").blur()

            // cidade
            var timeoutCidade = setInterval(() => {
                if (document.querySelector("#inputCidade").options.length > 1) {
                    document.querySelector("#inputCidade").options[
                        Math.floor(
                            Math.random() *
                            (document.querySelector("#inputCidade").options.length - 1)
                        ) + 1
                    ].selected = true;
                    clearInterval(timeoutCidade);
                    btn.focus();
                }
            }, 100);

            // cep
            document.querySelector("#inputCEP").value = 99999999;
            document.querySelector("#inputCEP").focus();
            document.querySelector("#inputCEP").dispatchEvent(new MouseEvent("keyup"));

            window._cache_[endpoint].splice(rand_number, 1);
            btn.focus();
        }
    }
    else if (type_register == "livro") {
        let endpoint = `/utils/mock/book`;
        let mock_book;
        if (!(endpoint in window._cache_) || window._cache_[endpoint].length == 0) {
            btn.disabled = true;
            let res = await fetch(endpoint);
            mock_book = await res.json();
            btn.disabled = false;
            window._cache_[endpoint] = mock_book;
        } else {
            mock_book = window._cache_[endpoint];
        }

        if (mock_book.length > 0) {
            var rand_number = Math.floor(Math.random() * mock_book.length);
            var data = mock_book[rand_number];

            // product_name
            document.querySelector("#inputProductName").value = data.product_name;
            document.querySelector("#inputProductName").focus();

            // unit_price
            document.querySelector("#inputUnitPrice").value = data.unit_price;
            document.querySelector("#inputUnitPrice").focus();
        }
    }
}

var formSubmitPessoa = (e) => {
    e.preventDefault();

    // get form
    var formdata = new FormData(e.target);

    // trim the values
    for (let key of formdata.keys()) {
        formdata.set(key, formdata.get(key).trim());
    }

    // validation
    var error = false;
    var error_message = [];

    if (formdata.get("form") == "cliente") {

        // full_name
        if (!formdata.get("full_name").length) {
            error = true;
            error_message.push({
                field: "full_name",
                message: "O nome não pode ser vazio.",
            });
        }

        // cpf
        {
            if (!formdata.get("cpf").length) {
                error = true;
                error_message.push({
                    field: "cpf",
                    message: "O cpf não pode ser vazio.",
                });
            }

            if (!validateCPF(formdata.get("cpf").replace(/\.|-/g, ""))) {
                error = true;
                error_message.push({
                    field: "cpf",
                    message: "O cpf é inválido.",
                });
            }
        }

        // birth_date
        if (!formdata.get("birth_date").length) {
            _date
            error = true;
            error_message.push({
                field: "birth_date",
                message: "A data de nascimento não pode ser vazia.",
            });
        }

        // id_genre
        if (formdata.get("id_genre") == 0) {
            error = true;
            error_message.push({
                field: "id_genre",
                message: "Selecione o gênero.",
            });
        }

        // id_state
        if (formdata.get("id_state") == 0) {
            error = true;
            error_message.push({
                field: "id_state",
                message: "Selecione o estado.",
            });
        }

        // id_city
        if (formdata.get("id_city") == 0) {
            error = true;
            error_message.push({
                field: "id_city",
                message: "Selecione a cidade.",
            });
        }

        // phone_number
        if (!formdata.get("phone_number").length) {
            error = true;
            error_message.push({
                field: "phone_number",
                message: "O número de contato não pode ser vazio.",
            });
        }

        // email
        if (
            !!formdata.get("email").length &&
            !validateEmail(formdata.get("email"))
        ) {
            error = true;
            error_message.push({
                field: "email",
                message: "O email é inválido.",
            });
        }

        // address
        if (!formdata.get("address").length) {
            error = true;
            error_message.push({
                field: "address",
                message: "O endereço não pode ser vazio.",
            });
        }
    }
    else if (formdata.get("form") == "livro") {
        // product_name
        if (!formdata.get("product_name").length) {
            error = true;
            error_message.push({
                field: "product_name",
                message: "O nome do livro não pode ser vazio.",
            });
        }

        // unit_price
        if (!formdata.get("unit_price").length) {
            error = true;
            error_message.push({
                field: "unit_price",
                message: "O preço do livro não pode ser vazio.",
            });
        }
    }

    if (error) {
        document.getElementsByName(error_message[0].field)[0].focus();
    }

    return [error, error_message];
}

var formSubmitOrder = (e) => {
    e.preventDefault();

    // get form
    var formdata = new FormData(e.target);

    // trim the values
    var keys_trimmed = []
    for (let key of formdata.keys()) {
        if (keys_trimmed.indexOf(key) != -1) continue;
        if (key.includes("[]") && key.indexOf("[]") == key.length - 2) {
            let values = formdata.getAll(key);
            formdata.delete(key);
            for (let v of values) {
                formdata.append(key, v.trim());
            }
        } else {
            formdata.set(key, formdata.get(key).trim());
        }
        keys_trimmed.push(key);
    }

    // validation
    var error = false;
    var error_message = [];

    // id_costumer
    if (!formdata.get("id_costumer")) {
        error = true;
        error_message.push({
            field: "id_costumer",
            message: "É necessário selecionar um paciente.",
        });
    }

    if (error) {
        document.getElementsByName(error_message[0].field)[0].focus();
    }

    return [error, error_message];
}
