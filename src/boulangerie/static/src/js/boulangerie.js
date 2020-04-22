let produits = [
	{ nom : "couque au chocolat", prix : 1, quantite : 0},
	{ nom : "croissant", prix : 1, quantite : 0},
	{ nom : "tarte au sucre", prix : 10.25, quantite : 0},
];

document.addEventListener('DOMContentLoaded', initialiserPage);

function initialiserPage() {
	let vueMagasin = new Vue({
		delimiters: ['[[', ']]'],
		el : "#magasin",
		data : {
			titre : {
				principal : "Bienvenue sur le site de la boulangerie",
				sousTitre : "Commande",
			},
			produits : produits,
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
}
