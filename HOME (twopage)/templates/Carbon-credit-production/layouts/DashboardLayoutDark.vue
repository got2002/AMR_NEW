<template>
	<div id="bg-repeat" class="bg-white h-full">
		
		<div class="flex overflow-hidden  pt-0">
			<SideBar />
			<div id="info-content" class="w-full h-full bg-white  lg:ml-64">
				<!-- <TopNav /> -->
				<main class="bg-white">
					<div class="p-12">
						<Nuxt />
					</div>
				</main>
			</div>
		</div>
	</div>
</template>
<style>
#bg-repeat{
	background-image: url("https://media-exp1.licdn.com/dms/image/C560BAQHMnA03XDdf3w/company-logo_200_200/0/1519855918965?e=2147483647&v=beta&t=J3kUMZwIphc90TFKH5oOO9Sa9K59fimgJf-s_okU3zs");
  background-repeat: repeat;
}
</style>