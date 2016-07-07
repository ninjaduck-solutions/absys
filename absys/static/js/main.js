function submitForm() {
  self.submit();
}

$(function() {
  var form = $('#anwesenheit_gruppe_formular')
  form.onclick = function() {form.submit()};
});
