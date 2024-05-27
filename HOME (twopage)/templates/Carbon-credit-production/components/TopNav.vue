<template>
	<div class="bg-white border-b shadow-sm w-full px-2">
		<div class="max-w-8xl mx-auto">
			<div class="grid grid-cols-12">
				<div class="col-span-3 flex items-center divide-x">
					<div @click="$router.push(localePath('/'))" class="flex items-center justify-start gap-2 cursor-pointer">
						<TGOLogo></TGOLogo>
						<!-- <span class="text-red-500 font-thin text-xs">*{{ $t("sidebar.testSystem") }}*</span> -->
					</div>
				</div>
				<template v-if="!loading">
					<div class="col-span-6 flex items-center justify-center gap-2 relative py-2">
						<div v-if="false" @click="$router.push(localePath('/showroom'))" :title="$t('button.showroom')" :class="{ 'text-tgo-teal-500': /(showroom)/.test($route.name) }" class="cursor-pointer flex flex-col items-center justify-center text-sm px-4 hover:text-tgo-teal-500 h-full relative">
							<IconShop width="20" height="20" />
							<p class="lg:block hidden text-sm">{{ $t("button.showroom") }}</p>
							<div v-if="/(showroom)/.test($route.name)" class="w-full h-1 rounded-t-md bg-tgo-teal-500 absolute z-10 -bottom-2 left-0"></div>
						</div>

						<div @click="$router.push(localePath('/document'))" :title="$t('button.document')" :class="{ 'text-tgo-teal-500': /(document)/.test($route.name) }" class="cursor-pointer flex flex-col items-center justify-center text-sm px-4 hover:text-tgo-teal-500 h-full relative">
							<IconDocument width="20" height="20" />

							<p class="lg:block hidden text-sm">{{ $t("button.document") }}</p>
							<div v-if="/(document)/.test($route.name)" class="w-full h-1 rounded-t-md bg-tgo-teal-500 absolute z-10 -bottom-2 left-0"></div>
						</div>

						<template v-if="isAuthenticated">
							<div @click="$router.push(localePath('/dashboard'))" :title="$t('topnav.admin')" v-if="[1, 99].includes($auth?.user?.role)" class="relative h-full cursor-pointer flex flex-col items-center justify-center text-sm px-4 hover:text-tgo-teal-500">
								<IconAdmin width="20" height="20" />
								<p class="lg:block hidden text-sm">{{ $t("topnav.admin") }}</p>
								<!-- <div v-if="/(dashboard)/.test($route.name)" class="w-full h-1 rounded-t-md bg-tgo-teal-500 absolute z-10 -bottom-2 left-0"></div> -->
							</div>
						</template>
					</div>

					<div class="col-span-3 flex items-center justify-end gap-2">
						<div class="flex items-center justify-center">
							<Language></Language>
						</div>

						<button v-if="false" @click="$router.push(localePath('/cart'))" class="flex items-center relative justify-center p-2 border rounded hover:bg-gray-100">
							<div v-if="getCart?.length !== 0" class="absolute z-10 w-5 h-5 bg-tgo-teal-400 rounded-full shadow-md -top-2 left-3 flex items-center justify-center text-xs text-white">
								{{ getCart?.length || 0 }}
							</div>
							<ShowroomCartIcon width="20" height="20" />
							<!-- <span class="lg:block hidden text-sm">{{ $t("topnav.cart") }}</span> -->
						</button>

						<div v-if="isAuthenticated">
							<TemplateUsername />
						</div>
						<div class="flex items-center gap-2 text-sm" v-if="!isAuthenticated">
							<div class="p-2 border bg-green-500 bg-opacity-10 hover:bg-opacity-20 border-green-500 text-green-500 rounded">
								<button class="h-6" @click="$router.push(localePath('/auth/register'))">{{ $t("topnav.open_new_account") }}</button>
							</div>
							<div class="p-2 border bg-tgo-teal-500 bg-opacity-10 hover:bg-opacity-20 border-tgo-teal-500 text-tgo-teal-500 rounded">
								<button class="h-6" @click="$router.push(localePath('/auth/signin'))">{{ $t("button.login") }}</button>
							</div>
							
						</div>
					</div>
				</template>
			</div>
		</div>
	</div>
</template>
	

<script>
import { mapGetters } from "vuex";

export default {
	data() {
		return {
			step: 1,
			cartItem: [],
			loading: true,
		};
	},
	computed: {
		...mapGetters(["isAuthenticated", "loggedInUser", "getCart"]),
		fullName() {
			return `${this.loggedInUser?.firstname} ${this.loggedInUser?.lastname[0] ?? ""}`;
		},
		monogram() {
			return `${this.loggedInUser?.firstname[0] ?? ""}${this.loggedInUser?.lastname[0] ?? ""}`;
		},
	},

	mounted() {
		this.loading = false;
		// this.cartItem = this.$auth.$storage.getLocalStorage("cart");
		// console.log(this.loggedInUser, this.isAuthenticated)
	},

	methods: {
		async logout() {
			await this.$auth.logout().then(() => {
				this.$toast.success(this.$t("toast.logout.success"));
				this.$router.push(this.localePath({ name: "/" }));
				setTimeout(this.$toast.clear, 3000);
			});
		},
	},
};
</script>
<style scoped>
.logo svg {
	max-width: 100%;
	width: 100%;
	max-height: 100px;
	height: auto;
	display: block;
}
</style>
