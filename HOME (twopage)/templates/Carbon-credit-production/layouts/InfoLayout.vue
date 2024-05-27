<template>
	<div>
	
		<div class="flex overflow-hidden bg-gray-100 pt-16 lg:pt-0">
			<SideBar2 />
			<div id="info-content" class="w-full  h-screen bg-gray-100 relative lg:ml-64">
					<TopNav />
				<main>
					<div class="p-12">
						<Nuxt />
					</div>
				</main>
			</div>
		</div>
	</div>
</template>