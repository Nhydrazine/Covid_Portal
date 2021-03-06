import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ShowAlignmentService } from './show-alignment-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Datafile, UploadFolder } from '../../models/datafile';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';
import { AlignmentObj, ResidueObj } from '../../models/alignment';

@Component({
    selector: 'list-files',
    providers: [ShowAlignmentService],
    templateUrl: './show-alignment.component.html',
    styleUrls: ['./show-alignment.component.scss']
})

export class ShowAlignmentComponent implements OnInit, OnDestroy{

    @Input()
    datafiles : UploadFolder[];
    allDatafiles : UploadFolder[];
    filterFilesOption:string;
    resultsAvailable:boolean;
    sub:Subscription;
    message:string;
    alignmentObjList:AlignmentObj[];
    displayAignmentObjList:AlignmentObj[];
    maxDisplayResidues :number;
    startPosition:number;
    endPosition:number;
    maxSliderValue:number;
    searchDataFilesString:string;
    positionSliderValue:number;

    ngOnDestroy(){
    }

    setSliderValue(){
      let positionSlider = document.getElementById('positionSlider') as HTMLInputElement;
      this.positionSliderValue = Number(positionSlider.value);
      for (let i = 0; i < this.alignmentObjList.length; i++){
        this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
        this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      }
    }

    ngOnInit() {
      console.log( " on init ");
      this.message = "";
      this.startPosition = 0;
      this.maxDisplayResidues = 60;
      this.endPosition = this.maxDisplayResidues;
      this.positionSliderValue = 0;
      this.showAlignmentService.showAlignment().then(alignmentObjList => {
         // console.log(alignmentObjList);
         this.alignmentObjList = alignmentObjList;
         for (let i = 0; i < this.alignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.alignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           // this.displayAignmentObjList[i].residueObjList = this.displayAignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
           this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
           // console.log(this.displayAignmentObjList[i].residueObjList);
         }
         // console.log(this.displayAignmentObjList);
      });
    }

    handleResidueClick(residueLabel, position){

    }

    constructor( private showAlignmentService: ShowAlignmentService,
               ) {
    };

}
