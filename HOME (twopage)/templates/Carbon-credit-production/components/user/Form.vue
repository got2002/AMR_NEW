<template>
	<div>
		<UserSkeletonLoading v-if="loading"></UserSkeletonLoading>
		<div id="user__form" class="grid grid-cols-2 gap-4" v-if="!loading">
			<div class="col-span-1">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.firstname") }}</label>
				<input :disabled="!edit" v-model="form.firstname" class="px-2 py-2 outline-none border-2 text-center w-full rounded" />
			</div>
			<div class="col-span-1">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.lastname") }}</label>
				<input :disabled="!edit" v-model="form.lastname" class="px-2 py-2 outline-none border-2 text-center w-full rounded" />
			</div>
			<div class="col-span-2">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.email") }}</label>
				<input :disabled="!edit" v-model="form.email" class="px-2 py-2 outline-none border-2 text-center w-full rounded" />
			</div>
			<div class="col-span-2">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.role") }}</label>
				<!-- <input v-model="form.roleText.text" class="px-2 py-2 outline-none border-2 text-center w-full" /> -->
				<v-select :disabled="!edit" v-model="form.roleText.text" :options="dropdowns.role" :reduce="(item) => item.value" label="text"></v-select>
			</div>
			<div class="col-span-2">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.organization") }}</label>
				<!-- <input v-model="form.organization" class="px-2 py-2 outline-none border-2 text-center w-full" /> -->
				<v-select :disabled="!edit" v-model="form.companyID" :options="dropdowns.organization" :reduce="(item) => item.value" :label="$i18n.locale"></v-select>
			</div>

			<div class="col-span-2">
				<label class="capitalize font-bold">{{ $t("user.create_page.form.permission") }}</label>
				<t-select v-if="edit" v-model="form.scopes" multiple :closeOnSelect="false" :options="dropdowns.userScopes" :hideSearchBox="true" valueAttribute="value" :textAttribute="$i18n.locale">
					<template slot="option" slot-scope="{ isSelected, option }">
						<div class="px-3 py-1" :class="{ 'bg-tgo-teal-300': isSelected }">
							<span>{{ option.raw[$i18n.locale] }}</span>
						</div>
					</template>
				</t-select>
				<div v-if="!edit" class="p-4 bg-gray-100 flex flex-wrap gap-2">
					<span v-for="scope in form.scopes" :key="scope" class="p-2 rounded bg-tgo-teal-500 shadow-sm text-sm text-white">{{ scopeValue(scope) }}</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form", "edit","loading"],
	data() {
		return {
			
			dropdowns: {
				role: [],
				organization: [],
				userScopes: [],
			},
		};
	},

	async mounted() {
		await this.getUserScopes();
		await this.getOrganization();
		await this.getRole();
		
	},
	methods: {
		scopeValue(value) {
			const scope = this._.find(this.dropdowns.userScopes, (item) => item.value === value);
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
		fullname(data) {
			return data.firstname + " " + data.lastname;
		},
		role(role) {
			switch (role) {
				case 0:
					return "User";
				case 1:
					return "Moderator";
				case 99:
					return "Admin";
				default:
					return "N/A";
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

<style>
#user__form .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;

	border: 2px solid rgba(168, 168, 168, 0.26) !important;

	border-radius: 4px !important;

	display: flex;
	padding: 8px 8px 8px 8px !important;
	white-space: normal;
}
</style>
