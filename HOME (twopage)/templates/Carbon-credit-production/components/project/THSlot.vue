<template>
	<th :rowspan="header.rowspan" class="px-3 bg-tgo-teal-500 text-sm font-medium text-theme-black-50 align-middle whitespace-nowrap py-3 ">
		<div class="w-full flex items-center gap-2" 
        :class="{
            'justify-start':header.align === 'left',
            'justify-center':header.align === 'center',
            'justify-end':header.align === 'right',

            }">
			{{header.name }}
			<template v-if="header.sortable">
				<div class="cursor-pointer" @click="setSortValue()">
					<font-awesome-icon icon="fas fa-sort" v-if="header.sortValue == 0" />
					<font-awesome-icon icon="fas fa-sort-down" v-else-if="header.sortValue == -1" />
					<font-awesome-icon icon="fas fa-sort-up" v-else-if="header.sortValue == 1" />
				</div>
			</template>
		</div>
	</th>
</template>

<script>
	export default {
        props:{
            header:{
                type:Object,
                require:true
            },
            
          
           
        },
        data(){
            return {
                sort:0
            }
        },
        methods:{
            setSortValue(){
                if(this.header.sortValue === 0) this.header.sortValue = 1
                else if(this.header.sortValue === 1) this.header.sortValue = -1
                else this.header.sortValue = 0
                this.$emit('setSortValue',this.header.sortValue)
            }
        }

    };
</script>

<style></style>
