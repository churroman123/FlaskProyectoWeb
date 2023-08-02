const btnAgregar = document.querySelector('.btn-agregar-tarjeta');
const seccionAgregar = document.querySelector('.registroTarjeta');
const btnCerrar = document.querySelector('.btn-cerrar-tarjeta');

btnAgregar.addEventListener('click', (e) => {

    seccionAgregar.classList.remove('hidden');

})

btnCerrar.addEventListener('click', (e) => {
    seccionAgregar.classList.add('hidden');
})
