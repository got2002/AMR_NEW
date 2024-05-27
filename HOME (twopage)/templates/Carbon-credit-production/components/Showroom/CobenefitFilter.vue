<template>
	<div class="grid grid-cols-3 gap-2">
		<div class="col-span-1">
			<label for="env">
				<div
					class="w-full border flex items-center justify-center gap-2 text-base py-2 rounded cursor-pointer"
					:class="{
						'bg-tgo-teal-500 text-white border-white': filter.coBenefit.includes('env'),
						'border-tgo-teal-500 text-tgo-teal-500': !filter.coBenefit.includes('env'),
					}"
				>
					<ShowroomLeafIcon :color="filter.coBenefit.includes('env')?'#fff':'#00b0d8'"/>
					<span>{{$t('showroom.filter.co_benefit.env')}}</span>
				</div>
			</label>
			<input type="checkbox" id="env" name="cobenefit" value="env" v-model="filter.coBenefit" hidden />
		</div>
		<div class="col-span-1">
			<label for="social">
				<div
					class="w-full border flex items-center justify-center gap-2 text-base py-2 rounded cursor-pointer"
					:class="{
						'bg-tgo-teal-500 text-white border-white': filter.coBenefit.includes('social'),
						'border-tgo-teal-500 text-tgo-teal-500': !filter.coBenefit.includes('social'),
					}"
				>
					<ShowroomUserIcon :color="filter.coBenefit.includes('social')?'#fff':'#00b0d8'"/>
					<span>{{$t('showroom.filter.co_benefit.social')}}</span>
				</div>
			</label>
			<input type="checkbox" id="social" name="cobenefit" value="social" v-model="filter.coBenefit" hidden />
		</div>
		<div class="col-span-1">
			<label for="eco">
				<div
					class="w-full border flex items-center justify-center gap-2 text-base py-2 rounded cursor-pointer"
					:class="{
						'bg-tgo-teal-500 text-white border-white': filter.coBenefit.includes('eco'),
						'border-tgo-teal-500 text-tgo-teal-500': !filter.coBenefit.includes('eco'),
					}"
				>
					<ShowroomCloudMoneyIcon :color="filter.coBenefit.includes('eco')?'#fff':'#00b0d8'"/>
					<span>{{$t('showroom.filter.co_benefit.eco')}}</span>
				</div>
			</label>
			<input type="checkbox" id="eco" name="cobenefit" value="eco" v-model="filter.coBenefit" hidden />
		</div>
	</div>
</template>

<script>
export default {
	props: ["filter"],
};
</script>

<style>
</style>