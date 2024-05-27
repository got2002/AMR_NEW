<template>
	<div>
		<UserSkeletonLoading v-if="loading"></UserSkeletonLoading>

		<div class="grid grid-cols-4 gap-4 text-sm" v-if="!loading">
			<div class="col-span-4 text-base font-bold border-b border-dashed">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 1 }) }}: {{ $t("user.view.form.profile_title") }}</p>
			</div>
			<div class="col-span-2">
				<label class="capitalize">{{ $t("user.create_page.form.firstname") }}</label>
				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ form.firstname }}</div>
			</div>
			<div class="col-span-2">
				<label class="capitalize">{{ $t("user.create_page.form.lastname") }}</label>
				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ form.lastname }}</div>
			</div>
			<div class="col-span-2">
				<label class="capitalize">{{ $t("user.create_page.form.email") }}</label>

				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ form.email }}</div>
			</div>
			<div class="col-span-2">
				<label class="capitalize">{{ $t("user.create_page.form.role") }}</label>
				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ role(form.role) }}</div>
			</div>
			<div class="col-span-4">
				<label class="capitalize">{{ $t("user.create_page.form.organization") }}</label>

				<div class="px-2 py-2 h-10 outline-none border-2 text-center w-full rounded">{{ organizationName(form.companyID) }}</div>
			</div>

			<div class="col-span-4">
				<label class="capitalize">{{ $t("user.create_page.form.permission") }}</label>

				<div class="p-2 bg-gray-100 flex flex-wrap gap-2 border rounded">
					<span v-for="scope in form.scopes" :key="scope" class="p-2 rounded bg-tgo-teal-500 shadow-sm text-sm text-white">{{ scopeValue(scope) }}</span>
				</div>
			</div>

			<div class="col-span-4 text-base font-bold border-b border-dashed">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 2 }) }}: {{ $t("user.view.form.account_title") }}</p>
			</div>

			<div class="col-span-4">
				<label class="capitalize">{{ $t("account.create_page.form.name") }}</label>

				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ form.account.accountName }}</div>
			</div>
			<div class="col-span-4">
				<label class="capitalize">{{ $t("account.create_page.form.accountTypes") }}</label>

				<div class="px-2 py-2 outline-none border-2 text-center w-full rounded">{{ AccountTypeText(form.account.accountTypeID) }}</div>
			</div>

			<div class="col-span-4 text-base font-bold border-b border-dashed">
				<p class="uppercase">{{ $t("user.view.form.part", { number: 3 }) }}: {{ $t("user.view.form.document") }}</p>
			</div>

			<div class="col-span-4">
				<div class="flex flex-wrap items-center gap-2">
					<template v-for="(doc, idx) in form.account.documents">
						<div :key="idx" class="w-20 cursor-pointer hover:underline" @click="showPDF(doc.src)">
							<div class="h-24 border rounded">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-20 h-20 text-center">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
								</svg>
							</div>
							<div class="break-words text-xs text-center">
								{{ doc.name }}
							</div>
						</div>
					</template>
				</div>

				<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form", "edit", "loading"],
	data() {
		return {
			dropdowns: {
				role: [],
				organization: [],
				userScopes: [],
				account_types: [],
			},
			pdfModal: false,
			pdfURL: "",
		};
	},

	async mounted() {
		await this.getUserScopes();
		await this.getOrganization();
		await this.getAccountTypes();
		await this.getRole();
	},
	methods: {
		showPDF(url) {
			this.pdfModal = true;
			this.pdfURL = process.env.baseUrl + url;
			// this.$swal('test')
			// window.open(url, '_blank');
		},
		scopeValue(value) {
			const scope = this._.find(this.dropdowns.userScopes, (item) => item.value === value);
			// console.log(scope);
			return scope[this.$i18n.locale];
		},
		organizationName(value) {
			const scope = this._.find(this.dropdowns.organization, (item) => item.value === value);
			// console.log(scope);
			if (!scope) return this.$t("undefined");
			return scope?.text;
		},
		AccountTypeText(value) {
			const scope = this._.find(this.dropdowns.account_types, (item) => item.value === value);
			// console.log(scope);
			return scope?.text;
		},
		async getRole() {
			const app = this;
			await this.$axios
				.$get(`/api/v1/dropdown/roles`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.role = resp;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getOrganization() {
			const app = this;

			await this.$axios
				.$get(`/api/v1/dropdown/organization`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.organization = resp;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getUserScopes() {
			const app = this;

			await this.$axios
				.$get(`/api/v1/dropdown/user/scopes`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.userScopes = resp;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getAccountTypes() {
			const app = this;

			await this.$axios
				.$get(`/api/v1/dropdown/account-types`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.account_types = resp;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		fullname(data) {
			return data.firstname + " " + data.lastname;
		},
		role(role) {
			switch (role) {
				case 0:
					return this.$t("account.filter.role.user");
				case 1:
					return this.$t("account.filter.role.moderator");
				case 99:
					return this.$t("account.filter.role.admin");
				default:
					return this.$t("undefined");
			}
		},
		dateLocale(date) {
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},
	},
};
</script>

<style></style>
