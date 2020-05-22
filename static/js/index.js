$(document).ready(function() {
    $('#form-request-tab').click(function () {
        document.getElementById('form-request').style.display = 'block';
        document.getElementById('submit-request').style.display = 'none';
    });

    $('#submit-request-tab').click(function () {
        document.getElementById('submit-request').style.display = 'block';
        document.getElementById('form-request').style.display = 'none';
    });

    $('#form-request-button').click(function () {
        var begin = $('#begin-input').val();
        var end = $('#end-input').val();
        var participantType = $('#participant-type-input').val();
        var participantId = $('#participant-id-input').val();
        $.post('/', {'type': 'form_request', 'begin': begin, 'end': end,
            'participant_type': participantType, 'participant_id': participantId}, function(data) {
            switch (data) {
                case 'begin_date_error':
                    alert('Необходимо ввести дату начала периода поиска');
                    break;
                case 'date_span_error':
                    alert('Временной промежуток поиска не должен превышать 30 дней');
                    break;
                case 'end_date_error':
                    alert('Дата окончания поиска не может быть раньше даты начала');
                    break;
                case 'participant_id_error':
                    alert('Укажите идентификатор участника сообщения');
                    break;
                case 'request_error':
                    alert('Что-то пошло не так. Попробуйте повторить попытку позже');
                    break;
            }
            window.location.href = '/';
        });
    });

    $('#submit-request-button').click(function () {
        var requestId = $('#request-id-input').val();
        $.post('/', {'type': 'submit_request', 'request_id': requestId}, function(data) {
            switch (data) {
                case 'request_id_absence_error':
                    alert('Укажите индентификатор задачи');
                    break;
                case 'request_id_type_error':
                    alert('Некорректный идентификатор задачи');
                    break;
                case 'request_error':
                    alert('Что-то пошло не так. Попробуйте повторить попытку позже');
                    break;
            }
            window.location.href = '/';
        });
    });
});