<template>
	<div class="relative">
		<div class="bg-black bg-opacity-40 w-full h-screen fixed z-20 top-0 left-0 transform duration-75" :class="{ flex: openMenu, hidden: !openMenu }"></div>
		
		
		<div class="w-full h-full fixed z-50 top-0 left-0 " :class="{ 'flex': openMenu, hidden: !openMenu }">
		
			<ul class="w-60 bg-white divide-y transition duration-500 ease-in-out transform" :class="{ 'delay-1000 translate-x-0': openMenu, '-translate-x-80': !openMenu }">
				<li class="w-full flex items-center justify-center p-4 flex-col space-y-2">
					<img src="/images/TGO_logo.png" class="w-1/2">
					<p class="text-sm font-bold">{{$t('project_name')}}</p>
				</li>
				<li class="nuxt-link-exact-active">
					<nuxt-link :to="localePath({ name: '/' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
						</svg>

						<!-- <font-awesome-icon icon="fa-regular fa-gauge" /> -->

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.home") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('dashboard')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'dashboard' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-speedometer" viewBox="0 0 16 16">
							<path d="M8 2a.5.5 0 0 1 .5.5V4a.5.5 0 0 1-1 0V2.5A.5.5 0 0 1 8 2zM3.732 3.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707zM2 8a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 8zm9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5zm.754-4.246a.389.389 0 0 0-.527-.02L7.547 7.31A.91.91 0 1 0 8.85 8.569l3.434-4.297a.389.389 0 0 0-.029-.518z" />
							<path fill-rule="evenodd" d="M6.664 15.889A8 8 0 1 1 9.336.11a8 8 0 0 1-2.672 15.78zm-4.665-4.283A11.945 11.945 0 0 1 8 10c2.186 0 4.236.585 6.001 1.606a7 7 0 1 0-12.002 0z" />
						</svg>
						<!-- <font-awesome-icon icon="fa-regular fa-gauge" /> -->

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.dashboard") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('projectManagement')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'project' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-file-earmark-text" viewBox="0 0 16 16">
							<path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5z" />
							<path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5L9.5 0zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.project") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('transactionManagement')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'transactions' })" class="text-base cursor-pointer font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap text-sm">{{ $t("sidebar.transaction") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('statistics')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'statistics' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pie-chart" viewBox="0 0 16 16">
							<path d="M7.5 1.018a7 7 0 0 0-4.79 11.566L7.5 7.793V1.018zm1 0V7.5h6.482A7.001 7.001 0 0 0 8.5 1.018zM14.982 8.5H8.207l-4.79 4.79A7 7 0 0 0 14.982 8.5zM0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8z" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.statistic") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('users')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'users' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-people" viewBox="0 0 16 16">
							<path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1h8zm-7.978-1A.261.261 0 0 1 7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002a.274.274 0 0 1-.014.002H7.022zM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM6.936 9.28a5.88 5.88 0 0 0-1.23-.247A7.35 7.35 0 0 0 5 9c-4 0-5 3-5 4 0 .667.333 1 1 1h4.216A2.238 2.238 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816zM4.92 10A5.493 5.493 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275zM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0zm3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" />
						</svg>
						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.user") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('accountManagement')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'accounts' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.accounts") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('organizationManagement')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'organization' })" class="text-base font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap text-sm">{{ $t("sidebar.organization") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('credentials')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'api' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-code-slash" viewBox="0 0 16 16">
							<path d="M10.478 1.647a.5.5 0 1 0-.956-.294l-4 13a.5.5 0 0 0 .956.294l4-13zM4.854 4.146a.5.5 0 0 1 0 .708L1.707 8l3.147 3.146a.5.5 0 0 1-.708.708l-3.5-3.5a.5.5 0 0 1 0-.708l3.5-3.5a.5.5 0 0 1 .708 0zm6.292 0a.5.5 0 0 0 0 .708L14.293 8l-3.147 3.146a.5.5 0 0 0 .708.708l3.5-3.5a.5.5 0 0 0 0-.708l-3.5-3.5a.5.5 0 0 0-.708 0z" />
						</svg>
						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.api") }}</span>
					</nuxt-link>
				</li>
				<li v-if="$auth.user?.scope.includes('logging')" class="nuxt-link-exact-active" @mouseup="$emit('openSidebar')">
					<nuxt-link :to="localePath({ name: 'logs' })" class="text-sm font-normal px-4 hover:bg-tgo-teal-500 hover:text-theme-white flex items-center p-2 group">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>

						<span class="ml-3 flex-1 whitespace-nowrap">{{ $t("sidebar.log") }}</span>
					</nuxt-link>
				</li>
			</ul>

			<button @click="$emit('openSidebar')" class="p-4 bg-white shadow-sm border h-14 transition duration-500 ease-in-out transform" :class="{ 'delay-1000 translate-x-0': openMenu, '-translate-x-80': !openMenu }">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	</div>
</template>

<script>
	export default {
		props: {
			openMenu:{
				type:Boolean,
				default:false
			}
		},
		data() {
			return {
				hiddenAll: false,
			};
		},
		watch: {
			openMenu(value) {
				const app = this
				if (!value) {
					setTimeout(() => {
						app.hiddenAll = true;
					}, 1000);
				}
				app.hiddenAll = false;
			},
		},
	};
</script>

<style></style>
