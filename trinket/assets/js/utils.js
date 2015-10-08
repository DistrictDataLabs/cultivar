/*
 * utils.js
 * Helper functions for global use in Topic Maps front-end apps
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Sun Aug 23 10:09:11 2015 -0500
 *
 * Dependencies:
 *  - jquery
 *  - underscore
 */

(function() {

  String.prototype.formalize = function () {
    return this.replace(/^./, function (match) {
      return match.toUpperCase();
    });
  };

  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };

  Array.prototype.range = function() {
    return [
      this.min(), this.max()
    ]
  }

  utils = {
    /*
     * Similar to humanize.intcomma - renders an integer with thousands-
     * separated by commas. Pass in an integer, returns a string.
     */
    intcomma: function(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    /*
     * Accepts an object and returns a GET query string (no ?)
     */
     encodeQueryData: function(data) {
      var ret = [];
      for (var d in data)
        ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
      return ret.join("&");
    },

    /*
     * Parses a string boolean and returns a bool type, especially Python bool str
     */
     parseBool: function(str) {
      if (typeof(str) === "boolean") {
        return str
      }

      return JSON.parse(
          str.toLowerCase()
            .replace('none', 'false')
            .replace('no','false')
            .replace('yes','true')
          );
    },
    getParam: function (key) {
      var value=RegExp(""+key+"[^&]+").exec(window.location.search);
      return unescape(!!value ? value.toString().replace(/^[^=]+./,"") : "");
    },
    /*
     * Pass in the selector for a form, this method uses jQuery's serializeArray
     * method to map the data in the form to an object for json.
     */
    formData: function(selector) {
      return _.object(_.map($(selector).serializeArray(), function(obj) {
        return [obj.name, obj.value];
      }));
    },

    cleanArray: function (actual){
      var newArray = new Array();
      for(var i = 0; i<actual.length; i++){
          if (actual[i]){
            newArray.push(actual[i]);
        }
      }
      return newArray;
    }

  }

})();
