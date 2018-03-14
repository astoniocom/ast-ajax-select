(function() {

  var $ = window.jQuery;
  
  $.fn.autocompleteselect = function(options) {
    return this.each(function() {
      var id = this.id,
          $this = $(this),
          $deck = $('#' + options["deck_id"]),
          fieldName = options["field_name"],
          keyName = options["key_name"],
          multiple = options["multiple"];

      function getKillerId(key) {
        return options["deck_id"] + '_' + key;
      }
          
      function receiveResult(event, ui) {
        var key = ui.item[keyName];

        if (!multiple)
          $deck.empty();
          
        if (!$( "#"+getKillerId(key) ).length) {
          addKiller(ui.item.repr, key);
          $this.val('');
          $deck.trigger('added', [ui.item.key, ui.item]);
          $this.trigger('change');
        }

        return false;
      }

      function addKiller(repr, key) {
        var killerId = getKillerId(key);
        $deck.append('<div id="' + killerId + '"><input type="hidden" name="'+fieldName+'" value="' + key + '" /><span class="ui-icon ui-icon-trash killer-button">X</span>' + repr + ' </div>');

        $('#' + killerId + ' .killer-button').click(function() {
          kill(key);
          $deck.trigger('killed', [key]);
        });
      }

      function kill(key) {
        var killerId = getKillerId(key);
        $('#' + killerId).fadeOut().remove();
      }

      options.select = receiveResult;
      $this.autocomplete(options);

      function reset() {
        $deck.empty();
        if (options.initial) {
          var initial = options.multiple && options.initial || [options.initial];

          $.each(initial, function(i, its) {
            addKiller(its[0], its[1]);
          });
        }
      }

      if (!$this.attr('data-changed')) {
        reset();
        $this.attr('data-changed', true);
      }

      $this.closest('form').on('reset', reset);

      $this.bind('didAddPopup', function(event, key, repr) {
        receiveResult(null, {item: {key: key, repr: repr}});
      });
    });
  };

  function addAutoComplete (inp, callback) {
    var $inp = $(inp),
        opts = JSON.parse($inp.attr('data-plugin-options'));
    // Do not activate empty-form inline rows.
    // These are cloned into the form when adding another row and will be activated at that time.
    if ($inp.attr('id').indexOf('__prefix__') !== -1) {
      // console.log('skipping __prefix__ row', $inp);
      return;
    }
    if ($inp.data('_ajax_select_inited_')) {
      // console.log('skipping already activated row', $inp);
      return;
    }
    // console.log('activating', $inp);
    callback($inp, opts);
    $inp.data('_ajax_select_inited_', true);
  }

  // allow html in the results menu
  // https://github.com/scottgonzalez/jquery-ui-extensions
  var proto = $.ui.autocomplete.prototype,
      initSource = proto._initSource;

  function filter(array, term) {
    var matcher = new RegExp($.ui.autocomplete.escapeRegex(term), 'i');
    return $.grep(array, function(value) {
      return matcher.test($('<div>').html(value.label || value.value || value).text());
    });
  }

  $.extend(proto, {
    /*_initSource: function() {
      if (this.options.html && $.isArray(this.options.source)) {
        this.source = function(request, response) {
          response(filter(this.options.source, request.term));
        };
      } else {
        initSource.call(this);
      }
    },*/
    _renderItem: function(ul, item) {
      return $('<li></li>')
        .data('item.autocomplete', item)
        .append($('<a></a>')['html'](item.label))
        .appendTo(ul);
    }
  });

  /* Called by the popup create object when it closes.
   * For the popup this is opener.dismissAddRelatedObjectPopup
   * Django implements this in RelatedObjectLookups.js
   * In django >= 1.10 we can rely on input.trigger('change')
   * and avoid this hijacking.
   */
  var djangoDismissAddRelatedObjectPopup = window.dismissAddRelatedObjectPopup || window.dismissAddAnotherPopup;
  window.dismissAddRelatedObjectPopup = function(win, newId, newRepr) {
    // Iff this is an ajax-select input then close the window and
    // trigger didAddPopup
    var name = window.windowname_to_id(win.name);
    var input = $('#' + name);
    if (input.data('ajax-select')) {
      win.close();
      // newRepr is django's repr of object
      // not the Lookup's formatting of it.
      input.trigger('didAddPopup', [newId, newRepr]);
    } else {
      // Call the normal django set and close function.
      djangoDismissAddRelatedObjectPopup(win, newId, newRepr);
    }
  }
  // Django renamed this function in 1.8
  window.dismissAddAnotherPopup = window.dismissAddRelatedObjectPopup;

  // activate any on page
  $(window).bind('init-autocomplete', function() {

    $('input[data-ajax-select=autocompleteselect]').each(function(i, inp) {
      if (inp.autocompleteready)
        return;
      inp.autocompleteready = true;
      addAutoComplete(inp, function($inp, opts) {
        $inp.autocompleteselect(opts);
      });
    });

  });

  $(document).ready(function() {
    // if dynamically injecting forms onto a page
    // you can trigger them to be ajax-selects-ified:
    $(window).trigger('init-autocomplete');
    // When adding new rows in inline forms, reinitialize and activate newly added rows.
    $(document)
      .on('click', '.inline-group ul.tools a.add, .inline-group div.add-row a, .inline-group .tabular tr.add-row td a', function() {
        $(window).trigger('init-autocomplete');
      });
  });

})();
