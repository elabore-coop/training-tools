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

        //Check if event product selection change
        var question_type = $(event.currentTarget).data('questionType');
        if (question_type == 'event_product' || question_type == 'multiple_event_products') {

            //Current question (for event products) id
            var event_product_question_id = event.currentTarget.name;

            //find event selector concerned by this event product question
            var event_selects = $('select[data-question-type="event"][data-event-product-question-id="'+event_product_question_id+'"]:visible');

            //find all event products selected in this question
            var event_product_ids = [];
            if (question_type == 'multiple_event_products') {
                // find event products selected in case of multiple event products question                
                event_product_ids = $('input[name="'+event_product_question_id+'"]:checked').map(function() {
                    return parseInt($(this).attr("value"));
                }).get();
            } else {
                // find event products selected in case of simple event product question         
                event_product_ids = [parseInt($(event.currentTarget).find(":selected").val())];
            }

            // populate concerned events selectors
            event_selects.each(function( index ) {
                var event_select = $(this);

                //Disable event selection
                event_select.prop('disabled', 'disabled');

                //Ajax : get new events
                ajax.jsonRpc('/survey_event/get_events_from_product', 'call', {                    
                    'product_ids': event_product_ids,
                    'only_visible_in_survey': event_select.data('only-visible-in-survey') === "True"
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

            })

        }


        var result = this._super.apply(this, arguments);
        return result;
    }
})

});
