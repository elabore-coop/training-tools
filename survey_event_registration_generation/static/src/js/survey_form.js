odoo.define('survey_event_registration_generation.survey.form', function (require) {
'use strict';

var SurveyFormWidget = require('survey.form');


SurveyFormWidget.include({    

    _prepareSubmitValues: function (formData, params) {
        var self = this;

        var result = this._super.apply(this, arguments);
        this.$('[data-question-type]').each(function () {
            if (['event','event_product'].includes($(this).data('questionType'))) {
                params[this.name] = this.value;
            }            
        });

        return result;
    },
   
})

});
