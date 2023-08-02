/*==========Abrir y cerrar carrito============*/
const btnCart = document.querySelector('.container-card-icon');
const containerCartProducts = document.querySelector('.container-cart-products');

btnCart.addEventListener('click', () => {
    containerCartProducts.classList.toggle('hidden-cart');
})

/*=======================*/

const cartInfo = document.querySelector('.cart-product');
const rowProduct = document.querySelector('.row-product');

//lista de todos los contenedores de procutos

const productsList = document.querySelector('.container-items');

//variable de arreglos de productos
let allProducts = []

const valorTotal = document.querySelector('.total-pagar');
const countProducts = document.querySelector('#contador-productos');

const cartEmpty = document.querySelector('.cart-empty');
const cartTotal = document.querySelector('.cart-total');


productsList.addEventListener('click', e => {
    if (e.target.classList.contains('add-to-cart')) {
        const product = e.target.parentElement

        const infoProduct = {
            cantidad: 1,
            ID: product.querySelector('p').textContent,
            titulo: product.querySelector('h2').textContent,
            precio: product.querySelector('span').textContent
        };

        // comprueba si en el carrito ya existe ese producto. regresa true o false
        const exist = allProducts.some(product => product.titulo === infoProduct.titulo)
        if (exist) {
            const products = allProducts.map(product => {
                //si se encuentra en el carrito lo seleccionara y regresara con la cantidad aumentada
                if (product.titulo === infoProduct.titulo) {
                    product.cantidad++;
                    return product;
                } else {
                    return product;
                }
            })
            allProducts = [...products];
        } else {
            //sino existe en elcarrito se agrega normalmente
            allProducts = [...allProducts, infoProduct];
        }


        showHTML();
    }
});
rowProduct.addEventListener('click', (e) => {
        if (e.target.classList.contains('icon-close')) {
            const product = e.target.parentElement;
            const ID = product.querySelector('p').textContent;


            allProducts = allProducts.filter(product => product.ID !== ID);
            showHTML();

        }
    })
    //funcion  para mostrar html

const showHTML = () => {

    if (!allProducts.length) {
        cartEmpty.classList.remove('hidden');
        rowProduct.classList.add('hidden');
        cartTotal.classList.add('hidden');
    } else {
        cartEmpty.classList.add('hidden');
        rowProduct.classList.remove('hidden');
        cartTotal.classList.remove('hidden');
    }

    //limpiar html
    rowProduct.innerHTML = '';

    let total = 0;
    let totalOfProducts = 0;

    allProducts.forEach(product => {
        const containerProduct = document.createElement('div');
        containerProduct.classList.add('cart-product');

        containerProduct.innerHTML = `
        <div class="info-cart-product">
            <span class="cantidad-producto-carrito">${product.cantidad}</span>
            <p style="display:none">${product.ID}</p>
            <h2 class="titulo-producto-carrito">${product.titulo}</h2>
            <span class="precio-producto-carrito">${product.precio}</span>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-close">
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18L18 6M6 6l12 12"
            />
        </svg> 
        `;

        rowProduct.append(containerProduct);

        total = total + parseFloat(product.cantidad * product.precio);
        totalOfProducts = totalOfProducts + product.cantidad;

    });



    valorTotal.innerText = `$${total}`;
    countProducts.innerText = totalOfProducts;

};

