/*
 * dataset.js
 * Javascript function that contains event-handlers for dataset page.
 *
 * Author:  Jane Radetska <raduga.jenya@gmail.com>
 * Created: Fri Jun 3 02:24:00 pm 2016 -0800
 *
 * Dependencies:
 *  - jquery
 *  - underscore
 */

(function($) {

  $(document).ready(function() {

      /*
       * Trigger for when a file is changed in the upload button
       * http://www.abeautifulsite.net/whipping-file-inputs-into-shape-with-bootstrap-3/
       */
      $(document).on('change', '.btn-file :file', function() {
          var input = $(this),
              numFiles = input.get(0).files ? input.get(0).files.length : 1,
              label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
          input.trigger('fileselect', [numFiles, label]);
      });

      // Handle the fileselect event
      $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
          $("#uploadIcon").removeClass("fa-upload").addClass("fa-spinner").addClass("fa-spin");
          $("#uploadForm").submit();
      });

      /*
       * Handle the dataset info editing forms
       */
      function handleDatasetInfo(event) {
        event.preventDefault();

        var form   = $(event.target);
        var url    = form.attr('action');
        var method = form.attr('method');
        var data   = utils.formData(form);

        console.log(url,method, data);

        // Clean the data from the form
        delete data.csrfmiddlewaretoken

        $.ajax({
            "url": url,
            "method": method,
            "data": JSON.stringify(data),
            "contentType": "application/json"
        }).done(function(data) {
            // Reload the page with the new information.
            location.reload(true);
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
      }

      // Register handlers
      $("#editDatasetInfoModal").submit(handleDatasetInfo);
      $("#editDatasetReadmeModal").submit(handleDatasetInfo);

      // click handler for star btn
      $('#star-btn').click(function(e) {

         $(this).toggleClass('active');
         $(this).attr('aria-pressed', $(this).hasClass('active'));

         console.log('fake ajax call to api');
      });

      // Ready to handle datasets!
      console.log("Ready to manage a dataset!");

  });

})(jQuery);
