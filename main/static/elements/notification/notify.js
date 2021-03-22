
class Notifications {

    constructor(message) {
    }

     check_notifications() {
         function Notify(message) {
            if (Notification.permission !== 'granted') {
                Notification.requestPermission().then((result) => {
                    if (result === 'denied')
                        console.log('Notification Permission Denied');
                    if (result === 'default')
                        console.log('Notification Permission Dismissed.');
                });
            } else {
                let notification = new Notification('MYDATA', {
                    icon: '/static/images/icon.png',
                    body: message,
                });
                // notification.onclick = function() {onclick()}
            }
         }

         $.ajax({
            url: '/ajax/check_notifications',
            data: {
            },
            dataType: 'json',

            success: function(data) {
                const arr = data['platform'];
                const platforms = ''.concat(arr);
                console.log(data);
                var message = 'Daily limit reached: ' + platforms;
                Notify(message)
            }
        });
    }






    //  Notify(message, onclick) {
    //
    //     if (Notification.permission !== 'granted') {
    //         Notification.requestPermission().then((result) => {
    //             if (result === 'denied')
    //                 console.log('Notification Permission Denied');
    //             if (result === 'default')
    //                 console.log('Notification Permission Dismissed.');
    //         });
    //     } else {
    //         let notification = new Notification('MYDATA', {
    //             icon: '/static/images/icon.png',
    //             body: message,
    //         });
    //         notification.onclick = function() {onclick()}
    //     }
    // }
}

