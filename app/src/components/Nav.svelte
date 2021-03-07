<script>
    import { stores } from "@sapper/app";
    const { page } = stores();

    export let segment;
</script>

<nav>
    <ul class="nav nav-tabs">
        <li class="nav-item" aria-current={segment === undefined ? "page" : undefined}>
            <a class="nav-link" href=".">Venda</a>
        </li>
        <!-- Navbar dropdown -->
        <li class="nav-item dropdown" aria-current={segment === "cadastro" ? "page" : undefined}>
            <a class="nav-link dropdown-toggle" href="#cadastros" id="navbarDropdown" role="button" data-mdb-toggle="dropdown" aria-expanded="false"> Cadastro </a>
            <!-- Dropdown menu -->
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <li aria-current={$page.path === "/cadastro/livro" ? "page" : undefined}>
                    <a class="dropdown-item" href="/cadastro/livro">Livro</a>
                </li>
                <li aria-current={$page.path === "/cadastro/cliente" ? "page" : undefined}>
                    <a class="dropdown-item" href="/cadastro/cliente">Cliente</a>
                </li>
            </ul>
        </li>
    </ul>
</nav>

<style>
    nav {
        border-bottom: 1px solid rgba(255, 62, 0, 0.1);
        font-weight: 300;
        padding: 0 1em;
    }

    ul {
        margin: 0;
        padding: 0;
    }

    /* clearfix */
    ul::after {
        content: "";
        display: block;
        clear: both;
    }

    [aria-current] {
        position: relative;
        display: inline-block;
    }

    .dropdown-menu [aria-current] {
        position: relative;
        display: block;
    }

    .dropdown-menu [aria-current] a {
        color: rgb(255, 62, 0);
    }

    [aria-current]::after {
        position: absolute;
        content: "";
        width: calc(100%);
        height: 2px;
        background-color: rgb(255, 62, 0);
        display: block;
        bottom: -1px;
    }

    a {
        text-decoration: none;
        display: block;
    }
</style>
