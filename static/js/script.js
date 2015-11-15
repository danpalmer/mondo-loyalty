$.extend({
  feature: function (bodyClass, callback) {
    if ($('body').hasClass(bodyClass)) {
      $(function() {
        callback();
      });
    }
  }
});

$.feature('f_link_scheme', function() {
  var schemeSelect = $('.js-scheme-select');
  var usernameField = $('.js-username-field');
  var passwordField = $('.js-password-field');

  function toggleUsernamePassword(show) {
    usernameField.parent().toggle(show);
    passwordField.parent().toggle(show);
  }

  toggleUsernamePassword(false);

  schemeSelect.on('change', function() {
    var selected = $($(this).find(':selected'));

    usernameField.siblings('label').text(selected.data('username-field'));
    passwordField.siblings('label').text(selected.data('password-field'));

    toggleUsernamePassword(selected.val().length);
  });
});
