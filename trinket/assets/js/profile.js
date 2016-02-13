/*
 * profile.js
 * Javascript for the user profile editing and management.
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Sat Feb 13 14:45:34 2016 -0500
 *
 * Dependencies:
 *  - jquery
 *  - trinket utils
 */

(function($) {
  $(document).ready(function() {

    // Configure the profile application
    var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});
    console.log("Profile application ready");

    var passwordForm = $("#setPasswordForm");
    var profileForm  = $("#editProfileForm");
    var userDetail   = profileForm.attr('action');

    // When setPasswordModal is closed - reset the setPasswordForm
    $('#setPasswordModal').on('hidden.bs.modal', function (e) {
      passwordForm.removeClass('has-error');
      $('#passwordHelp').text("");
      $('#setPasswordForm')[0].reset();
    });

    // Handle setPasswordForm submission
    passwordForm.submit(function(e) {
      e.preventDefault();
      // Get form data
      var data = {
        'password': $('#txtPassword').val(),
        'repeated': $('#txtRepeated').val()
      }
      // Validate the data
      if (data.password != data.repeated) {
        passwordForm.addClass('has-error');
        $('#passwordHelp').text("passwords do not match!");
        return
      } else if (data.password.length < 6) {
        passwordForm.addClass('has-error');
        $('#passwordHelp').text("password must be at least 6 characters");
        return
      }
      // POST the change password data
      var passwordEndpoint = passwordForm.attr('action');
      $.post(passwordEndpoint, data, function(result) {
        $("#setPasswordModal").modal('hide');
      });
      return false;
    });

    // Handle the profile submission
    profileForm.submit(function(e) {
      e.preventDefault();
      // Get the form data
      var data = utils.formData(profileForm);

      data.profile = {
          "biography": data.biography,
          "organization": data.organization,
          "location": data.location,
          "twitter": data.twitter,
          "linkedin": data.linkedin
      };

      delete data.biography;
      delete data.organization;
      delete data.location;
      delete data.twitter;
      delete data.linkedin;

      $.ajax({
          "url": userDetail,
          "method": "PUT",
          "data": JSON.stringify(data),
          "contentType": "application/json"
      }).done(function(data) {
          // Update DOM with data requested
          $("#profileFullName").text(data.first_name + " " + data.last_name);
          $("#profileUsername").text(data.username);
          $("#profileEmail").text(data.email);
          $("#profileOrganization").text(data.profile.organization);
          $("#profileLocation").text(data.profile.location);
          $("#profileTwitter").text("@" + data.profile.twitter);
          $("#profileTwitterA").attr("href", "https://twitter.com/" + data.profile.twitter + "/");
          $("#profileLinkedIn").text(data.last_name + " Profile");
          $("#profileLinkedInA").attr("href", data.profile.linkedin);
          $("#editProfileModal").modal("hide");
      }).fail(function(xhr) {
          data = xhr.responseJSON;
          // Set the error
          $.each(data, function(key, val) {
              var field = $("#"+key);
              field.parent().addClass("has-error");
              field.parent().find('.help-block').text(val);
          });
      });
      return false;
    });

    // Reset form on close
    $("#editProfileModal").on("hide.bs.modal", function(e) {
      resetEditProfileModal();
    });

    // Helper function to reset edit profile modal
    function resetEditProfileModal() {
      profileForm.find('.form-group').removeClass("has-error");
      profileForm.find('.help-block').text("");
    }
  });
})(jQuery);
