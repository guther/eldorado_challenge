<style>
.select-input {
  position: relative;
}
.select-label {
  position: absolute;
  top: -10px;
  left: 10px;
  background: #fff;
  padding: 0px 4px;
  font-size: 13px;
  font-weight: 400;
  z-index: 1;
}
</style>

<script>
import { onMount } from "svelte";
import { each } from "svelte/internal";

onMount(() => {
  document
    .querySelector("#form_new_report")
    .addEventListener("submit", formSubmit);
});

const formSubmit = (e) => {
  e.preventDefault();

  // get form
  var formdata = new FormData(e.target);

  // trim the values
  for (let key of formdata.keys()) {
    formdata.set(key, formdata.get(key).trim());
    console.log(key, formdata.get(key));
  }

  // validation
  var error, error_message;
  [error, error_message] = window.formSubmitRelatorio(e);

  // show toast
  document.querySelector("#toast-container") &&
    document.querySelector("#toast-container").remove();

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
      document.querySelector(
        "#toast-container .toast-message"
      ).innerHTML = alert_msg;
    }
  } else {
    var table_container = document.querySelector("div.table-responsive");
    table_container.innerHTML = "";

    var spinner = e.target.querySelector("button[type='submit'] span.spinner");
    if (spinner) spinner.style.display = "inline-block";
    var btn_save_text = document.querySelector("#btn_save_text");
    var bkp_btn_save_text;
    if (btn_save_text) {
      bkp_btn_save_text = btn_save_text.textContent;
      btn_save_text.textContent = "Gerando...";
      btn_save_text.disabled = true;
    }

    fetch(`/search/relatorio/`, {
      method: "POST",
      body: formdata,
    })
      .then((response) => {
        spinner && (spinner.style.display = "none");
        btn_save_text &&
          (btn_save_text.textContent = bkp_btn_save_text) &&
          (btn_save_text.disabled = false);

        if (response.ok) {
          var contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            return response.json().then((json) => {
              Object.keys(json).includes("error") &&
                toastr.error(json.error, "Atenção!", {
                  closeButton: true,
                  tapToDismiss: true,
                  preventDuplicates: true,
                });
              if (Object.keys(json).includes("msg")) {
                var new_table = document.createElement("table");
                new_table.setAttribute("id", "search_results");
                new_table.classList.add("table");
                table_container.appendChild(new_table);

                var values = [];
                for (let register of json.msg) {
                  let data_atendimento = register.data_atendimento
                    .split("T")[0]
                    .split("-")
                    .reverse()
                    .join("/");
                  let nome_paciente = register.nome_paciente;
                  let cpf_paciente = register.cpf_paciente;
                  let nome_medico = register.nome_medico;
                  let crm_medico = register.crm_medico;
                  let anotacao = register.anotacao.replace(/\n/g, "<br>");

                  values.push([
                    data_atendimento,
                    nome_paciente,
                    cpf_paciente,
                    nome_medico,
                    crm_medico,
                    anotacao,
                  ]);
                }
                jQuery("#search_results").innerHTML = "";
                jQuery("#search_results").DataTable({
                  data: values,
                  columns: [
                    { title: "Data" },
                    { title: "Paciente" },
                    { title: "CPF do Paciente" },
                    { title: "Médico" },
                    { title: "CRM do Médico" },
                    { title: "Anotação" },
                  ],
                  language: {
                    decimal: "",
                    emptyTable: "Nenhum registro válido na tabela",
                    info:
                      "Mostrando de _START_ a _END_ de um total de _TOTAL_ atendimentos",
                    infoEmpty:
                      "Mostrando 0 até 0 de um total de 0 atendimentos",
                    infoFiltered:
                      "(filtrados de um total de _MAX_ atendimentos)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ atendimentos",
                    loadingRecords: "Carregando...",
                    processing: "Processando...",
                    search: "Busca:",
                    zeroRecords: "Nenhum resultado encontrado",
                    paginate: {
                      first: "Primeiro",
                      last: "Último",
                      next: "Próximo",
                      previous: "Anterior",
                    },
                    aria: {
                      sortAscending: ": ordem ascendente",
                      sortDescending: ": ordem descendente",
                    },
                  },
                });
                document.querySelector("#form_new_register").reset();
              }

              console.log(json);
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
        console.error(
          "There has been a problem with your fetch operation: " + error.message
        );
      });
  }
};
</script>

<svelte:head>
  <title>Relatório de Atendimento</title>
</svelte:head>

<h1>Relatório de Atendimento</h1>

<form id="form_new_report">
  <div class="d-md-flex mt-4 mb-3 col-12">
    <div class="select-input col-md-3">
      <input type="date" class="form-control" name="data_inicial" required />
      <label for="selectMedico" class="select-label">Data Inicial</label>
    </div>

    <div class="select-input col-md-1 text-center">até</div>

    <div class="select-input col-md-3">
      <input type="date" class="form-control" name="data_final" required />
      <label for="selectMedico" class="select-label">Data Final</label>
    </div>
  </div>

  <div class="col-12">
    <button type="submit" class="btn btn-primary"
      ><span
        class="spinner spinner-border spinner-border-sm"
        role="status"
        aria-hidden="true"
        style="display:none"></span>
      <span id="btn_save_text">Gerar Relatório</span>
    </button>
  </div>
</form>

<div class="table-responsive mt-5"></div>
