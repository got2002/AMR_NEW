<template>
	<div class="pt-2 pb-4">
		<div class="w-full my-6">
			<span class="font-bold text-2xl text-theme-black-300">{{ $t("api.page_title") }}</span>
		</div>
		<div class="grid grid-cols-3 gap-6">
			<ApiCredentialsVolume :title="$t('api.stat_title.all')" :value="stat.total" :icon="1"></ApiCredentialsVolume>
			<ApiCredentialsVolume :title="$t('api.stat_title.enable')" :value="stat.active" :icon="2"></ApiCredentialsVolume>
			<ApiCredentialsVolume :title="$t('api.stat_title.disable')" :value="stat.inactive" :icon="3"></ApiCredentialsVolume>
		</div>
		<div>
			<section class="pt-6 pb-4 flex flex-row justify-between">
				<div class="flex flex-row gap-2 items-center">
					<div class="relative inline-flex flex-wrap items-stretch">
						<select v-model="limit" @change="getApi()" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="relative inline-flex flex-wrap items-stretch">
						<select v-model="filter" @change="getApi()" class="text-sm text-center border border-gray-200 px-2 py-1 rounded bg-white outline-none">
							<option :value="null">{{ $t("api.filter.status.all") }}</option>
							<option :value="0">Draft</option>
							<option :value="1">Released</option>
							<option :value="2">Terminated</option>
							<option :value="3">Temporary closed</option>
						</select>
					</div>
					<div class="relative flex bg-theme-white">
						<span class="z-10 h-full leading-snug font-normal text-center text-defireGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-1">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</span>
						<input type="text" v-model="searchText" @change="getApi()" :placeholder="$t('api.filter.search')" class="text-sm text-center py-1.5 pl-10 pr-4 border border-gray-200 rounded outline-none" />
					</div>
				</div>
				<nuxt-link :to="localePath({ name: 'api-create' })" class="px-2 py-1 bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-sm rounded text-white flex items-center gap-1">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
					</svg>

					{{ $t("button.create") }}
				</nuxt-link>
			</section>
			<ApiTable :dataList="dataList" @reload="getApi" />
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
		<loadingCarbon v-if="isLoading"></loadingCarbon>
	</div>
</template>

<script>
	export default {
		layout: "DashboardLayout",
		name: "APIIndex",
		middleware: ["auth"],
		data() {
			return {
				stat: {},
				searchText: "",
				filter: null,
				current_page: 1,
				status: "",
				dataList: [],
				isLoading: false,
				meta: {},
				limit: 10,
			};
		},
		async mounted() {
			await this.getStatApi();
			await this.getApi();
			// this.$axios.$post(`/api/v1/line/auth`).then((resp) => {
			// 	console.log(resp);
			// 	this.$axios.$post(resp).then((resp2) => {
			// 		console.log(resp2);
			// 	});
			// });
		},
		methods: {
			getStatApi() {
				const app = this;
				this.$axios.$get(`/api/v1/stats/apps`).then((resp) => {
					// console.log(resp);
					app.stat = resp;
				});
			},
			getApi() {
				const app = this;
				let filter = "";
				this.isLoading = true;
				if (this.searchText !== null && this.searchText !== "") filter += `&search=${this.searchText}`;
				if (this.filter !== null && this.filter !== "") filter += `&status=${this.filter}`;
				if (this.limit !== null && this.limit !== "") filter += `&limit=${this.limit}`;
				this.$axios
					.$get(`/api/v1/app?page=${this.current_page}` + filter)
					.then((resp) => {
						// console.log(resp);
						app.meta = resp.meta;
						app.dataList = resp.data;
						app.isLoading = false;
					})
					.catch((err) => {
						console.log(err);
						app.isLoading = false;
					});
			},
			async loadRequestByPage(pageNumber) {
				this.current_page = pageNumber;
				console.log(`[Info] - Request Page Number ${pageNumber}`);
				await this.getApi();
			},
		},
	};
</script>

<style></style>
