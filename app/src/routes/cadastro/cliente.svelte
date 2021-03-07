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

        return { estados, generos };
    }
</script>

<script>
    import { onMount } from "svelte";
    onMount(() => {
        document.querySelectorAll(".form-outline").forEach((formOutline) => {
            new mdb.Input(formOutline).init();
        });
        VMasker(document.querySelector("#inputCPF")).maskPattern("999.999.999-99");
        VMasker(document.querySelector("#inputCEP")).maskPattern("99.999-999");
        VMasker(document.querySelector("#inputTelefone")).maskPattern("(99) 99999-9999");
    });

    async function getCidades(obj) {
        let inputCidade = document.querySelector("#inputCidade");
        let inputEstado = document.querySelector("#inputEstado");
        let ufEstado = inputEstado.options[inputEstado.selectedIndex].value;
        if (ufEstado) {
            let cidades;
            let endpoint = `http://localhost:5000/utils/cities/${ufEstado}`;
            if (!(endpoint in window._cache_)) {
                inputCidade.disabled = true;
                let res = await fetch(endpoint);
                cidades = await res.json();
                inputCidade.disabled = false;
                window._cache_[endpoint] = cidades;
            } else {
                cidades = window._cache_[endpoint];
            }
            return cidades;
        } else {
            inputCidade.options[0].selected = true;
        }
    }

    let cidades = [];

    export let estados;
    export let generos;
</script>

<svelte:head>
    <title>Cadastro de Clientes</title>
</svelte:head>

<h5>Dados pessoais</h5>
<div class="col-12">
    <div class="form-outline">
        <input type="text" id="inputName" name="full_name" class="form-control" maxlength="255" required />
        <label for="inputName" class="form-label">Nome</label>
    </div>
</div>
<div class="col-md-4">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputCPF" name="cpf" placeholder="999.999.999-99" maxlength="14" required onkeydown="return onlyNumbers(event);" />
        <label for="inputCPF" class="form-label">CPF</label>
    </div>
</div>
<div class="col-md-4">
    <div class="form-outline select-input">
        <input type="date" class="form-control " id="inputDataNascimento" name="birth_date" required />
        <label for="inputDataNascimento" class="select-label">Data de Nascimento</label>
    </div>
</div>
<div class="col-md-4">
    <div class="select-input">
        <select id="inputSexo" name="id_genre" class="form-select">
            <option value="0" selected>-</option>
            {#each generos as genero}
                <option value={genero.id}>{genero.genre_name}</option>
            {/each}
        </select>
        <label for="inputSexo" class="select-label">Sexo</label>
    </div>
</div>

<div class="col-md-6">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputTelefone" name="phone_number" maxlength="15" placeholder="(99) 99999-9999" required onkeydown="return onlyNumbers(event);" />
        <label for="inputTelefone" class="form-label">Número de Contato</label>
    </div>
</div>

<div class="col-md-6">
    <div class="form-outline">
        <input type="email" name="email" class="form-control" id="inputEmail" />
        <label for="inputEmail" class="form-label">Email</label>
    </div>
</div>

<div class="col-12">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputEndereco" name="address" maxlength="255" required placeholder="Rua, nº da residência, bairro" />
        <label for="inputEndereco" class="form-label">Endereço</label>
    </div>
</div>
<div class="col-12">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputComplemento" name="complement" placeholder="Apartamento, bloco, conjunto" maxlength="255" />
        <label for="inputComplemento" class="form-label">Complemento</label>
    </div>
</div>
<div class="col-md-4">
    <div class="select-input">
        <select
            id="inputEstado"
            name="id_state"
            class="form-select"
            on:blur={async (obj) => {
                cidades = await getCidades(obj);
            }}
        >
            <option value="0" selected>-</option>
            {#each estados as estado}
                <option value={estado.uf}>{estado.state_name}</option>
            {/each}
        </select>
        <label for="inputEstado" class="select-label">Estado</label>
    </div>
</div>
<div class="col-md-5">
    <div class="select-input">
        <select id="inputCidade" name="id_city" class="form-select">
            <option value="0" selected>-</option>
            {#if cidades && cidades.length > 0}
                {#each cidades as cidade}
                    <option value={cidade.id}>{cidade.city_name}</option>
                {/each}
            {/if}
        </select>
        <label for="inputCidade" class="select-label">Cidade</label>
    </div>
</div>
<div class="col-md-3">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputCEP" name="postal_code" placeholder="99.999-999" maxlength="10" onkeydown="return onlyNumbers(event);" />
        <label for="inputCEP" class="form-label">CEP</label>
    </div>
</div>
