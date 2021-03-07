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
            new mdb.Input(formOutline).update();
        });
    });
    export let estados;
    export let generos;
</script>

<svelte:head>
    <title>Cadastro de Livro</title>
</svelte:head>

<h5>Informações do livro</h5>

<div class="col-md-6">
    <div class="form-outline">
        <input type="text" class="form-control" id="inputProductName" name="product_name" required maxlength="255" />
        <label for="inputProductName" class="form-label">Título</label>
    </div>
</div>

<div class="col-md-6">
    <div class="form-outline">
        <input type="number" min="0.00" max="10000.00" step="0.01" class="form-control" id="inputUnitPrice" name="unit_price" required maxlength="10" />
        <label for="inputUnitPrice" class="form-label">Preço (R$)</label>
    </div>
</div>
