(async function () {
    'use strict';

    // variable qui contient l'état du panier, en particulier la liste des produits
    const commande = {
        id: undefined,
        produits: [],
    };

    // récupère les données initiales de commande et produits du panier
    const response = await axios.get('/produits/commande/detail');
    majCommande(response.data.commande);

    /**
     * Met à jour la variable commande sur base des données reçues du serveur.
     * Cela met en particulier à jour la liste des produits et leurs quantités.
     */
    function majCommande(dataCommande) {
        commande.id = dataCommande.id;
        for (const dataProduit of dataCommande.produits) {
            let produit = commande.produits.find(p => p.id === dataProduit.id);
            if (produit) {
                // si le produit existe déjà, on le met à jour
                Object.assign(produit, dataProduit);
            } else {
                // sinon on le crée
                produit = Object.assign({}, dataProduit);
                commande.produits.push(produit);
                // nouvelle quantite dans l'interface, non reçue par le serveur
                // variable séparée pour permettre d'annuler sans écraser l'ancienne valeur
                produit.nouvelle_quantite = produit.quantite;
            }
        }
    }

    /**
     * Met à jour un produit et sa quantité dans le panier.
     */
    async function postPanier(produit_id, quantite) {
        const response = await axios.post('/produits/commande/ajouter', {
            produit_id,
            quantite,
        })
        majCommande(response.data.commande);
    }

    // initialise Vue sur la modal de produit
    const vm = new Vue ({
        el: '#produit_modal',
        data: {
            produit: undefined, // par défault, modal fermée donc aucun produit
        },
        methods: {
            /**
             * Ajoute 1 à la nouvelle quantité.
             */
            ajouter() {
                this.produit.nouvelle_quantite++;
            },
            /**
             * Retire 1 à la nouvelle quantité.
             */
            enlever() {
                if(this.produit.nouvelle_quantite > 0) {
                    this.produit.nouvelle_quantite--;
                }
            },
            /**
             * Met à jour le panier sur base de la nouvelle quantité, et redirige vers le panier.
             */
            async allerPanier() {
                await postPanier(this.produit.id, this.produit.nouvelle_quantite);
                window.location.href = "/commande";
            },
            /**
             * Met à jour le panier sur base de la nouvelle quantité, et ferme la modal.
             */
            async continuerAchat() {
                await postPanier(this.produit.id, this.produit.nouvelle_quantite);
                $('#produit_modal').modal('hide');
            },
        },
    });

    // va chercher les données à afficher dans la modal en fonction du produit choisi
    $('#produit_modal').on('show.bs.modal', async function (ev) {
        const button = $(ev.relatedTarget);
        const produit_id = parseInt(button.data('id'));
        let produit = commande.produits.find(p => p.id === produit_id);
        if (!produit) {
            // si le produit n'existe pas encore dans le panier, on l'ajoute avec une quantité 0
            // (le reste du code de ce fichier ne fonctionne que si le produit est dans le panier)
            await postPanier(produit_id, 0);
            produit = commande.produits.find(p => p.id === produit_id);
        }
        // cliquer sur "ajout au panier" propose toujours d'augmenter la quantité existante de 1 par défaut
        produit.nouvelle_quantite = produit.quantite + 1;
        // indique à Vue quel est le produit à afficher
        vm.produit = produit;
    });

    // tant que les nouvelles données ne sont pas chargées, ne pas afficher l'ancien produit
    $('#produit_modal').on('hidden.bs.modal', function (ev) {
        vm.produit = undefined;
    });
})();
