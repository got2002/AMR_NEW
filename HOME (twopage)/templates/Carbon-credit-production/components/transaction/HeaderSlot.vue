<template>
	<th class="px-3 text-sm font-medium text-theme-black-50 align-middle whitespace-nowrap py-3">
		<!-- <div class="w-full flex items-center justify-center relative text-shadow-sm">
			{{header.name }}
			<template v-if="header.sortable">
				<div class="absolute z-10 -right-2 cursor-pointer" @click="setSortValue('project_id', index)">
					<font-awesome-icon icon="fas fa-sort" v-if="sort[index] == 0" />
					<font-awesome-icon icon="fas fa-sort-down" v-else-if="sort[index] == 1" />
					<font-awesome-icon icon="fas fa-sort-up" v-else-if="sort[index] == -1" />
				</div>
			</template>
		</div> -->
        {{header.name }}
	</th>
</template>

<script>
	export default {
        props:{
            header:{
                type:Object,
                require:true
            },
            // index:{
            //     type:Number,
            //     require:true
            // },
            // sort:{
            //     type:Array,
            //     default:()=>[]
            // }
        }
    };
</script>

<style></style>
