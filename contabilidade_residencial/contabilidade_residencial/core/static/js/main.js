$(document).ready(function () {
  /** --------- ADICIONAR PESSOA ---------- */
  let adicionar_pessoa_propriedades_id = 1;
  $("#adicionar_pessoa form button[type=button]").click(function (e) {
    adicionar_pessoa_propriedades_id++;
    $("#propriedades_adicionais").append(`
        <div class="campos_propriedade">
            <label for="propriedades_chave_${adicionar_pessoa_propriedades_id}">Chave</label>
            <input type="text" name="propriedades_chave[]" id="propriedades_chave_${adicionar_pessoa_propriedades_id}" />
            <label for="propriedades_valor_${adicionar_pessoa_propriedades_id}">Valor</label>
            <input type="text" name="propriedades_valor[]" id="propriedades_valor_${adicionar_pessoa_propriedades_id}" />
        </div>`);
  });

  /** --------- ADICIONAR REGISTRO ---------- */
  $("#adicionar_registro #pessoa").change(function (e) {
    $.get(`api/banco?pessoa_id=${e.target.value}`, (data) => {
      const bancos = JSON.parse(data)
      $("#adicionar_registro #banco").attr("disabled", false);
      $("#adicionar_registro #banco").html(
        '<option value="">Selecione um Banco</option>'
      );
      console.log(bancos);
      bancos.forEach((banco) => {
        $("#adicionar_registro #banco").append(
          `<option value="${banco.pk}">${banco.fields.apelido}</option>`
        );
      });
    });
  });

  /** --------- EDITAR REGISTRO ---------- */
  $("#editar_registro #pessoa").change(function (e) {
    $.get(`api/banco?pessoa_id=${e.target.value}`, (data) => {
      const bancos = JSON.parse(data)
      $("#editar_registro #banco").attr("disabled", false);
      $("#editar_registro #banco").html(
        '<option value="">Selecione um Banco</option>'
      );
      console.log(bancos);
      bancos.forEach((banco) => {
        $("#editar_registro #banco").append(
          `<option value="${banco.pk}">${banco.fields.apelido}</option>`
        );
      });
    });
  });
});
