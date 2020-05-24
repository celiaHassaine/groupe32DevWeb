(function () {
'use strict'

    //Toutes les clés doivent être déclaré pour que vue puisse les observer correctement
    const produit = {
        id: undefined,
        nom: undefined,
        prix: undefined,
        image: undefined,
        quantite: 0,
    };

    // Requête vers le back-end
    const postProduits = produit_id => {
        return axios.post('/produits/detail', {
            produit_id,
            quantite: 1,
        }).then(response => {
            Object.assign(produit, response.data.produit);
        });
    };

    new Vue ({
        el: '#produit_modal',
        data: {
            produit,
        },
        methods: {
            ajouter(produit) {
                produit.quantite++;
            },

            enlever(produit) {
                if(produit.quantite > 0) {
                    produit.quantite--;
                }
            },

            total() {
                const reducer = (total, produit) => total + produit.prix * produit.quantite;
                return produits.reduce(reducer, 0);
            }
        },
    });

    // va chercher les données à afficher dans la modal en fonction du produit choisi
    $('#produit_modal').on('show.bs.modal', function (ev) {
        const button = $(ev.relatedTarget);
        const produit_id = button.data('id');
        postProduits(produit_id);
    });

    //Tant que les données ne sont pas chargé n'affiche pas l'ancien produit
    $('#produit_modal').on('hidden.bs.modal', function (ev) {
        produit.id = undefined;
    });
})();
