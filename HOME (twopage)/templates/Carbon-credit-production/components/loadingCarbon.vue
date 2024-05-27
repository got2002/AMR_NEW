<template>
	<div style="z-index: 4999" class="fixed -top-10 left-0 w-full h-full  flex flex-col items-center justify-center bg-white bg-opacity-50 backdrop-filter backdrop-blur-sm">
		<div class="flex relative w-20 animate-bounce">
			<div class="w-full">
				<img src="/images/TGO_logo.png" class="w-full" />
			</div>
		</div>
		<span class="text-xl font-light mt-5 ">{{ $t("loading") }}</span>
	</div>
</template>

<script>
	export default {};
</script>

<style></style>
