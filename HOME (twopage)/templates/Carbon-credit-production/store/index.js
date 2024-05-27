import VuexPersistence from "vuex-persist";

export const state = () => ({
	appSecretKey: "",
	cart: [],
	cartErr: null,
	cartLoading: false,
});
export const getters = {
	isAuthenticated(state) {
		return state.auth.loggedIn;
	},

	loggedInUser(state) {
		return state.auth.user;
	},
	getSecretKey(state) {
		return state.appSecretKey;
	},
	getCart(state) {
		return state.cart;
	},
	getCartErr(state) {
		return state.cartErr;
	},
	getCartLoading(state) {
		return state.cartLoading;
	},
};
export const mutations = {
	setSecretKey(state, payload) {
		state.appSecretKey = payload;
	},
	addCart(state, payload) {
		const find = state.cart.findIndex((item) => item.blockId === payload.blockId);

		if (find === -1) {
			state.cart.push(payload);
		} else {
			state.cart[find].quantity = state.cart[find].quantity + payload.quantity;
		}
		state.cartErr = null;
	},

	removeCart(state, payload) {
		state.cart.splice(payload, 1);
		state.cartErr = null;
	},
	setCart(state, payload) {
		// console.log(payload);
		state.cart[payload.index].quantity = payload.data;
		state.cartErr = null;
	},
	setCartErr(state, payload) {
		state.cartErr = payload;
		state.cart = payload?.data.cart??state.cart;
	},
	clearCart(state) {
		state.cart = [];
		state.cartErr = null;
	},
	setCartLoading(state, payload) {
		state.cartLoading = payload;
	},
};
export const actions = {
	async addCart({ commit, state }, payload) {
		await commit("addCart", payload);
		await updateCart(state.cart, commit, this);
	},
	async removeCart({ commit, state }, payload) {
		await commit("removeCart", payload);
		await updateCart(state.cart, commit, this);
	},
	async setCart({ commit, state }, payload) {
		await commit("setCart", payload);
		await updateCart(state.cart, commit, this);
	},
	async clearCart({ commit }) {
		await commit("clearCart");
	},
};

async function updateCart(data, commit, app) {
	commit("setCartLoading", true);
	await app.$axios
		.$post(`/api/v1/cart`, {
			items: data,
		})
		.then((resp) => {
			// console.log(resp);
			app.$toast.success(app.$t('toast.cart.update'));

			setTimeout(app.$toast.clear, 3000);
			commit("setCartLoading", false);
		})
		.catch((err) => {
			commit("setCartLoading", false);
			commit("setCartErr", err.response);
		});
}

const vuexPersist = new VuexPersistence({
	/* options */
	// key: 'your-key', // Same as the key used in the plugin configuration
	// storage: window.localStorage // or window.sessionStorage or any other storage implementation
	// Additional options as needed
});

export const plugins = [vuexPersist.plugin];
