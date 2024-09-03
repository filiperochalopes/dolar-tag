document.getElementById('type').addEventListener('change', function () {
  const selectElement = this;
  selectElement.className = ''; // Remove classes antigas
  selectElement.classList.add(selectElement.value); // Adiciona classe correspondente ao valor
});

// Adiciona classe correta ao elementos select com base no valor padrão
document.getElementById('type').classList.add(document.getElementById('type').value);
