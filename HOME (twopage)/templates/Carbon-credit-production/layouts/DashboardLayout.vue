<template>
	<div class="h-full bg-theme-black-50">
		<TopNavV2 @openSidebar="openSidebar = !openSidebar"/>
		<TabMobile :openMenu="openSidebar" @openSidebar="openSidebar = false"></TabMobile>
		<div class="grid 2xl:grid-cols-12 lg:grid-cols-10 grid-cols-10 w-full h-full ">
			<SideBar class="2xl:block md:block hidden 2xl:col-span-2 lg:col-span-2 col-span-2 " />
			<div class="2xl:col-span-10 lg:col-span-8 col-span-10 bg-theme-black-50  flex-grow h-full w-full 2xl:px-20 2xl:py-10 px-5 py-10">
				<Nuxt />
			</div>
		</div>
		
	</div>
</template>
<script>
export default {
	data(){
		return{
			openSidebar:false,
		}
	}
}
</script>
