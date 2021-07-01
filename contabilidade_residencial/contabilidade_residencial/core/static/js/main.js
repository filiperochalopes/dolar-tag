function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}

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
      const bancos = JSON.parse(data);
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
      const bancos = JSON.parse(data);
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

  /** --------- EXCLUIR REGISTRO ---------- */
  $("button.excluir_registro").click(function (e) {
    if (confirm("Tem certeza que deseja excluir esse registro?")) {
      const id = $(this).data("id");
      $.ajax({
        url: `/api/registro/${id}`,
        type: "DELETE",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function () {
          window.location.reload();
        },
      });
    }
  });

  /** --------- FILTRAR REGISTRO ---------- */
  $("input[type=checkbox].pessoa_filtro").change(function () {
    const pessoaId = $(this).data("pessoa-id"),
      checked = $(this).is(":checked");
    console.log(pessoaId, checked);
    $(`input[type=checkbox].banco_filtro.pessoa_${pessoaId}`).prop(
      "checked",
      checked
    );
  });
  
  $("#filtro_registro_mes_atual").click(function () {
    const queryInput = $("input[name=q]");
    let queryInputValue = queryInput.val();
    const hoje = new Date();
    const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    const formatarData = (data) =>
    data.getDate() + "/" + (data.getMonth() + 1) + "/" + data.getFullYear();
    const mesAtualRange = `${
      formatarData(primeiroDiaMes)}-${formatarData(hoje)
    }`;
    console.log(hoje, primeiroDiaMes)
    if (queryInputValue.match(/\d{1,2}\/\d{1,2}\/\d{2,4}/)) {
      // Substitui a data atual pelo mês atual
      queryInputValue = queryInputValue.replace(
        /\d{1,2}\/\d{1,2}\/\d{2,4}/,
        mesAtualRange
      );
    } else {
      // Apenas adiciona o mês atual
      queryInputValue = `${queryInputValue} ${mesAtualRange}`;
    }
    queryInput.val(queryInputValue);
  });

});
