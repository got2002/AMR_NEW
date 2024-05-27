<template>
	<div class="w-full p-2 flex items-center gap-2 text-sm relative border hover:bg-gray-100 cursor-pointer rounded" v-clickOutside="()=>openDropdown = false" @click="openDropdown = !openDropdown">
		<div class="w-6 h-6 rounded-full bg-tgo-teal-100 border border-tgo-teal-500 text-tgo-teal-500 text-xs flex items-center justify-center">{{monogram}}</div>
		<span class="xl:block hidden text-sm">{{fullName}}</span>
		<IconArrowDown />
		<div v-show="openDropdown" class="absolute z-50 right-0 top-12 w-full shadow-lg min-w-max">
			<ul 
			data-aos="fade-down"
			data-aos-delay="50"
			data-aos-duration="1000"
			class="divide-y w-full bg-white">
				<li v-if="$auth.user.accountID !== null" class="px-2 py-2 w-full hover:bg-gray-100">
					<a :href="localePath('/home/credit')" class="flex items-center gap-2 w-full">
						<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
						</svg>

						<p>{{ $t("topnav.my_account") }}</p>
					</a>
				</li>
				<li v-else class="px-2 py-2 w-full hover:bg-gray-100">
					<a :href="localePath('/home/openAccount')" class="flex items-center gap-2 w-full">
						<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
						</svg>

						<p>{{ $t("topnav.new_account") }}</p>
					</a>
				</li>
				<li class="px-2 py-2 w-full hover:bg-gray-100">
					<a :href="localePath('/profile')" class="flex items-center gap-2 w-full">
						<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" />
						</svg>

						<p>{{ $t("button.edit_profile") }}</p>
					</a>
				</li>
				<li class="px-2 py-2 w-full hover:bg-gray-100">
					<button @click="logout" class="flex items-center gap-2 w-full text-red-500">
						<svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
						</svg>
						{{ $t("button.logout") }}
					</button>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
import AOS from "aos";
import "aos/dist/aos.css";
import vClickOutside from "v-click-outside";
export default {
    
    directives: {
		clickOutside: vClickOutside.directive,
	},
    computed: {
		...mapGetters(["isAuthenticated", "loggedInUser", "getCart"]),
		fullName() {
			return `${this.loggedInUser?.firstname} ${this.loggedInUser?.lastname}`;
		},
		monogram() {
			return `${this.loggedInUser?.firstname[0] ?? ""}${this.loggedInUser?.lastname[0] ?? ""}`;
		},
	},
    
	data: () => {
		return {
			openDropdown: false,
		};
	},
	mounted() {
		AOS.init();
	},
    methods:{
        async logout() {
			await this.$auth.logout().then(() => {
				this.$toast.success(this.$t("toast.logout.success"));
				this.$router.push(this.localePath({ name: "/" }));
				setTimeout(this.$toast.clear, 3000);
			});
		},
    }
};
</script>

<style>
</style>