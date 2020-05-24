
/*import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)*/

let produits = [
	{ nom : "couque au chocolat", prix : 1, quantite : 0},
	{ nom : "croissant", prix : 1, quantite : 0},
	{ nom : "tarte au sucre", prix : 10.25, quantite : 0},
];


var commandes = new Vue ({
    delimiters: ['[[', ']]'],
    el : "#commandes",
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

/*
var nouvelle = new Vue({
    el : "#magasin",
    data : {
        infos: []
    },
    mounted () {
        axios
            .get('http://127.0.0.1:8000/api/news/')
            .then(response => this.infos = response.data.slice())
            .catch(error => {
                console.log(error)
                this.errored = true
            })
            .finally(() => this.loading = false)
    }
});
*/
