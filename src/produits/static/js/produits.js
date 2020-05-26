(async function () {
    'use strict';

    // variable qui contient l'état du panier, en particulier la liste des produits
    const commande = {
        id: undefined,
        commande_produits: [],
        prix_total: 0,
    };

    // récupère les données initiales de commande et produits du panier
    const response = await axios.get('/produits/commande/detail');
    majCommande(response.data.commande);

    /**
     * Met à jour la variable commande sur base des données reçues du serveur.
     * Cela met en particulier à jour la liste des produits et leurs quantités.
     */
    function majCommande(data_commande) {
        commande.id = data_commande.id;
        commande.prix_total = data_commande.prix_total;
        for (const data_commande_produit of data_commande.commande_produits) {
            let commande_produit = commande.commande_produits.find(cp => cp.id === data_commande_produit.id);
            if (commande_produit) {
                // si le produit existe déjà, on le met à jour
                Object.assign(commande_produit, data_commande_produit);
            } else {
                // sinon on le crée
                commande_produit = Object.assign({
                    // nouvelle quantite dans l'interface, non reçue par le serveur
                    // variable séparée pour permettre d'annuler sans écraser l'ancienne valeur
                    nouvelle_quantite: data_commande_produit.quantite
                }, data_commande_produit);
                commande.commande_produits.push(commande_produit);
            }
        }
    }

    /**
     * Met à jour un produit (sur base de commande_produit) et sa quantité dans le panier.
     */
    async function postPanierCommandeProduit(commande_produit, quantite) {
        const response = await axios.post('/produits/commande/ajouter', {
            produit_id: commande_produit.produit.id,
            valeur_ids: commande_produit.produit.produit_attributs.map(pa => parseInt(pa.valeur_selectionee)),
            quantite: parseInt(quantite),
        })
        majCommande(response.data.commande);
    }

    /**
     * Met à jour un produit (première combinaison de valeur) et sa quantité dans le panier.
     */
    async function postPanierPremierProduit(produit_id, quantite) {
        const response = await axios.post('/produits/commande/ajouter', {
            produit_id,
            quantite: parseInt(quantite),
        })
        majCommande(response.data.commande);
    }

    if ($('#produit_modal').length > 0) {
        // initialise Vue sur la modal de produit
        const vm = new Vue ({
            el: '#produit_modal',
            data: {
                commande_produit: undefined, // par défault, modal fermée donc aucun produit
            },
            methods: {
                /**
                 * Ajoute 1 à la nouvelle quantité.
                 */
                ajouter() {
                    this.commande_produit.nouvelle_quantite++;
                },
                /**
                 * Retire 1 à la nouvelle quantité.
                 */
                enlever() {
                    if(this.commande_produit.nouvelle_quantite > 0) {
                        this.commande_produit.nouvelle_quantite--;
                    }
                },
                /**
                 * Met à jour le panier sur base de la nouvelle quantité, et redirige vers le panier.
                 */
                async allerPanier() {
                    await postPanierCommandeProduit(this.commande_produit, this.commande_produit.nouvelle_quantite);
                    window.location.href = "/commande";
                },
                /**
                 * Met à jour le panier sur base de la nouvelle quantité, et ferme la modal.
                 */
                async continuerAchat() {
                    await postPanierCommandeProduit(this.commande_produit, this.commande_produit.nouvelle_quantite);
                    $('#produit_modal').modal('hide');
                },
            },
        });

        // va chercher les données à afficher dans la modal en fonction du produit choisi
        $('#produit_modal').on('show.bs.modal', async function (ev) {
            const button = $(ev.relatedTarget);
            const produit_id = parseInt(button.data('id'));
            let commande_produit = commande.commande_produits.find(cp => cp.produit.id === produit_id);
            if (!commande_produit) {
                // si le produit n'existe pas encore dans le panier, on l'ajoute avec une quantité 0
                // (le reste du code de ce fichier ne fonctionne que si le produit est dans le panier)
                await postPanierPremierProduit(produit_id, -1);
                commande_produit = commande.commande_produits.find(cp => cp.produit.id === produit_id);
            }
            // cliquer sur "ajout au panier" propose toujours d'augmenter la quantité existante de 1 par défaut
            commande_produit.nouvelle_quantite = commande_produit.quantite + 1;
            // indique à Vue quel est le produit à afficher
            vm.commande_produit = commande_produit;
        });

        // tant que les nouvelles données ne sont pas chargées, ne pas afficher l'ancien produit
        $('#produit_modal').on('hidden.bs.modal', function (ev) {
            vm.commande_produit = undefined;
        });
    }

    if ($('#commandes').length > 0) {
        // initialise Vue sur le panier
        $('#commandes').removeClass('d-none');
        var commandes = new Vue ({
            el: "#commandes",
            data: {
                commande,
            },
            methods: {
                ajouter(commande_produit) {
                    commande_produit.quantite++;
                    postPanierCommandeProduit(commande_produit, commande_produit.quantite);
                },

                enlever(commande_produit) {
                    if(commande_produit.quantite > 0) {
                        commande_produit.quantite--;
                    }
                    postPanierCommandeProduit(commande_produit, commande_produit.quantite);
                },
            },
        });
    }
})();
