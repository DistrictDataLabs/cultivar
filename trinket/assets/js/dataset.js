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

      var starsAPIbaseUrl = $("#stars-api-base-url").val();

      // click handler for star btn
      $('#star-btn').click(function() {

         // get some info about situation: btn obj, dataset_id, action user wants to perform
         var star_btn = $(this);
         star_btn.prop('disabled', true);
         var dataset_id = star_btn.data('dataset-id');
         var wantToStar = !star_btn.hasClass('active');

         // construct request based on action: star or unstar
         var request_dict = {
            "contentType": "application/json"
         };
         if (wantToStar) {
             request_dict['method'] = 'POST';
             request_dict['url'] = starsAPIbaseUrl;
             request_dict['data'] = JSON.stringify({'dataset_id': dataset_id});
         } else {
             request_dict['method'] = 'DELETE';
             request_dict['url'] = starsAPIbaseUrl + dataset_id + '/';
         }

         // perform ajax request & react to it's success by changing appearance of star btn
         $.ajax(request_dict).done(function() {
            star_btn.toggleClass('active');
            star_btn.attr('aria-pressed',star_btn.hasClass('active'));
             console.log('Dataset starred successfully');
         }).fail(function(xhr) {
            console.log('Error during dataset starring: ' + xhr.responseJSON);
         }).always(function(){
             star_btn.prop('disabled', false);
         });

      });

      // Ready to handle datasets!
      console.log("Ready to manage a dataset!");

  });

})(jQuery);
