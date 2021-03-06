import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListStrainsRoutingModule } from './list-strains-routing.module';
import { ListStrainsComponent } from './list-strains.component';
import { FormsModule } from '@angular/forms';
import { ListFilesFilterPipe} from '../../pipes/list-files-filter.pipe';

import { ReactiveFormsModule } from '@angular/forms';

import { NgxDatatableModule } from '@swimlane/ngx-datatable';

@NgModule({
    imports: [CommonModule,
              ListStrainsRoutingModule,
              FormsModule,
              ReactiveFormsModule,
              NgxDatatableModule
            ],

    declarations: [ListStrainsComponent, ListFilesFilterPipe]
})
export class ListStrainsModule {}
