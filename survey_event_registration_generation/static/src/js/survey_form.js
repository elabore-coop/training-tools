odoo.define('survey_event_registration_generation.survey.form', function (require) {
'use strict';

var SurveyFormWidget = require('survey.form');
var ajax = require('web.ajax');
var core = require('web.core');

var _t = core._t;
var _lt = core._lt;


SurveyFormWidget.include({    

    _prepareSubmitValues: function (formData, params) {
        var self = this;

        var result = this._super.apply(this, arguments);
        this.$('[data-question-type]').each(function () {
            if (['event','event_product'].includes($(this).data('questionType'))) {
                params[this.name] = this.value;
            } else if ($(this).data('questionType') == 'multiple_event_products') {
                $(this).find('input:checked').each(function () {
                    if (this.value !== '-1') {
                        params = self._prepareSubmitAnswer(params, this.name, this.value);
                    }
                });
            }
        });

        return result;
    },

    _onChangeChoiceItem: function (event) {        
        var event_select = $('select[data-question-type="event"]:visible')
        
        //Check if event product selection change
        if ($(event.currentTarget).data('questionType') == 'event_product') {
            //Check if event selection visible
            if (event_select) {
                //Disable event selection
                event_select.prop('disabled', 'disabled');

                //Get event product id
                var eventProductId = parseInt($(event.currentTarget).find(":selected").val())

                //Ajax : get new events
                ajax.jsonRpc('/survey_event/get_events_from_product', 'call', {                    
                    'product_id': eventProductId,                   
                }).then((new_events) => {
                    // Delete old events
                    $(event_select).find('option').remove()

                    $(event_select).append(new Option(_t('Please select...')))

                    //Populate new events
                    for (var i in new_events) {
                        $(event_select).append(new Option(new_events[i].name, new_events[i].id))
                    }
                    
                    //Enable event selection
                    event_select.prop('disabled', false);
                });
                
            }
        }


        var result = this._super.apply(this, arguments);
        return result;
    }
})

});
