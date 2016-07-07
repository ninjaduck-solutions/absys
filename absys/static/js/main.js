$(function() {
  var form = $('#anwesenheit_gruppe_formular')
  if (form.length) {
    $('select[name="gruppe_id"]').on('change', function() {form.submit()});
    form.find('[type=submit]').hide();
  }
});
