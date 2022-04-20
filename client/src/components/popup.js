import Swal from 'sweetalert2';

const Popup = () => {
    return Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    });
};

const error = message => {
    Popup().fire({
        title: message,
        icon: 'error'
    })
};

const success = message => {
    Popup().fire({
        title: message,
        icon: 'success'
    });
};

export {
    error,
    success
};