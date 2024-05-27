<template>
	<div class="w-full space-y-4">
		<div v-if="!loading">
			<ShowroomFilter @fetch="filterApply" :limit="limit" :filter="filter" />
		</div>
		<div class="grid grid-cols-12 gap-4" v-if="!loading">
			<ShowroomProjectCard v-for="item in project" :key="item._id" :data="item" />
		</div>
		<div class="grid grid-cols-12 gap-4" v-if="loading">
			<ShowroomProjectCardLoad v-for="i in 8" :key="i" />
		</div>
		<div v-if="project.length == 0 && !loading" class="w-full py-8 text-center bg-gray-100">
			{{$t('no_data')}}
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
	</div>
</template>

<script>
export default {
	name: "Showroom",
	layout: "MainLayout",
	data() {
		return {
			meta: {
				pages: 1,
				current_page: 1,
				total: 1,
			},
			project: [],
			current_page: 1,
			filter: {
				projectType: "",
				vintageYear: "",
				availability: {
					min: 0,
					max: null,
				},
				priceRange: {
					min: 0,
					max: null,
				},
				coBenefit: [],
			},
			limit:{},
			search: "",
			openFilter: true,
			loading: true,
		};
	},
	mounted() {
		this.getProject();
	},
	
	methods: {
		filterApply(filter) {
			this.filter = filter;
			this.getProject();
		},
		
		loadRequestByPage(pageNumber) {
			this.getProject(pageNumber);
		},
		getProject(page = 1) {
			this.current_page = page;
			const app = this;
			let vintageyear = "";
			if (this.filter.vintageYear !== null && this.filter.vintageYear !== "") {
				vintageyear = this.$dayjs(this.filter.vintageYear).format("YYYY-MM-DD");
			}

			this.loading = true;
			this.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			this.$swal.showLoading();
			this.$axios.$get(`/api/v1/showroom?page=${this.current_page}&projectType=${this.filter.projectType}&vintageYear=${vintageyear}&availableTonneMin=${this.filter.availability.min}&availableTonneMax=${this.filter.availability.max}&priceMin=${this.filter.priceRange.min}&priceMax=${this.filter.priceRange.max}&coBenefit=${this.filter.coBenefit}&search=${this.search}`).then((resp) => {
				app.project = resp.data;
				app.meta = resp.meta;
				app.limit = resp.meta.limit;

				app.loading = false;
				app.$swal.close();
			});
		},
	},
};
</script>

<style>
</style>