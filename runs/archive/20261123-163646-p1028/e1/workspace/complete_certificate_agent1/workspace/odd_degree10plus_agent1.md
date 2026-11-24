# Odd-order reduction: all even degrees d>=10
The following argument bounds every connected simple even-d-regular graph, independentlyof parityn:
 d Ruv <= [(d²+15d-8)/(2(d+1)²)] n -(d³+4d²+15d-8)/(2(d+1)²).
For d10 coefficient1 and constant771/121>278/45; for d>=12 coefficient<=1 and constant>d/2+1>=7. Therefore it is strictlybelow every requiredodd normalizedtarget n-c, c<=278/45.

## Ordered chord-count lemma
Let bipartitegraph have ordered parts A1..Ar andB1..Bl, and satisfy: edgesAiBj,AkBh withi<k,j>h implyk=i+1,j=h+1. Ifv=r+l>=2, it hasatmost3v/2-2edges. Inductonv. Thev2caseisobvious. Ifavertexhasdegree<=1, deleteit anduseinduction (remainingv>=2), givingevenstrongerbound. Otherwise allverticesdegree>=2. LetA1's first/lastneighborsbeBj,Bk. BjhasanotherneighborAh,h>=2. Theinversionforcesh2,k=j+1, soA1hasexactlytwoneighborsBj,Bj+1, andBjhasexactlyneighborsA1,A2. Ifj>1, B1's twoneighborsbothafterA1giveaninversionwithA1Bj; onehasindex>=3, impossible. Thusj1. DeletingA1,B1 deletesexactly3edges; remainingorderedgraphhastheproperty, soinductiongives3+3(v-2)/2-2=3v/2-2. (Ifonepartemptytheboundtriviallyholdswhenv>=2.)

## Local block bound
LetB bea two-connectedblock, b itsorder, allitsdegreesatmostd, and Delta=sum_x(d-deg_Bx). Fixu,v. ChooseashortestcycleCcontainingthem, lengthc. Neitherendpointcanhaveachord, because thatshortensonearc. Chordsjoininteriorsofthetwoarcs (a same-arcchordshortens). Twoinvertedcrosschords mustoccupyconsecutiveverticesonbotharcs: otherwise switchingarcsatthesetwochords givesashorteruvcycle. Thusthechordlemmayieldsatmost3(c-2)/2-2chordswhenc>=4.
AnoutsidevertexhasatmostthreeCneighborsoneacharc; otherwiseitsfirst/lastneighborscanbejoinedthroughitin2edges, shorteningthecycle. Therefore totaldegreeincidencesonC areatmost2c+3c-10+6(b-c)=6b-c-10. Ontheotherhandtheyareatleastdc-Delta. Hence
 (d+1)c<=6b-10+Delta.
Ifc3andb>=4, everyoutsidevertexhasatmost3Cneighbors. Thusdc-Delta<=6+3(b-3)=3b-3, whichimpliesthesameboundbecauseb>=4. Theonlyexcludedcaseisb3, handledbelow.
Adjacentedgeeffective resistanceinsideB isatleast2/(d+1): contractallothervertices; theresultingdirectedgeisinparallelwithtwoseriesbundlesofatmostd-1unitresistors. Foster'sidentitysum_edgesR_e=b-1andtheresistancetriangleinequalityalongbothuvarcsgive
 2Ruv<=sum_(e in C)R_e<=b-1-2(m-c)/(d+1),
where2m=db-Delta. Substitutecycleboundtoobtain
 Ruv<=A b+Q Delta-C0,
 A=(d+13)/(2(d+1)²), Q=(d+3)/(2(d+1)²), C0=1/2+10/(d+1)².
Forb3, Bistriangle, Delta=3(d-2), andtheRHSsimplifiesto d(d+2)/(d+1)²>=2/3=Ruv. Sotheboundholdsforallblocks.

## Reassemble blockpath
Everyblockofaneven-regulargraphhasallitsdegreesEVEN: theedgesleavinganycomponentatacutvertexformacutandhenceareeven, andtheblock'sdegreesfollow. Inparticulartherearenobridgesandallblocksare2connectedoforder>=3.
Forfixedu,v followtheunique block-cutpath, withkblocks. Assignalloffpathvertices to thepathblockwheretheirsubtreeattaches. Letw_i beassignedorderincludingtheblock'sownvertices. Then sumw_i=n+k-1.
An offpathportx hasblockdegreea>=2, soitsdeficitd-a<=d-2. Everyoffpathcomponentattachedtherecontainsatleastd+1vertices: togetherwithxitisagraphwhereallnonrootverticeshavedegreedandtherootdegreebetween2andd-2; simplicityforcesorder>=d+2. Thus theterm A*(assignedsidevertices) morethanpaysitsdeficit Q*(d-a), since A(d+1)>Q(d-2). Differentoffpathportsreceive disjointvertices.
Thetwoblocksmeetingatanyinternalpatharticulationhavecombineddeficitd there, because theirdegrees sumtod unlessoffpathcomponentsalsoattachthere. Anyextraoffpathdeficitiscoveredbytheprecedingsidecharge. Endpointarticulations arehandledidentically asoffpathports. Consequently sum_i[A b_i+Q Delta_i]<=A(n+k-1)+Qd(k-1).
Alsoeachw_i>=d+1: ifthereisnooffpathport, atmosttwoverticesofitsblockhavedegreelessthand, andb_i>=3, henceatleastonefull-degreevertexforcesb_i>=d+1; ifanoffpathportexists, itsassignedsidealonehas>=d+1vertices. Thereforek<=(n-1)/d.
Seriesresistancelawandthelocalboundyield
 Ruv<=A(n+k-1)+Qd(k-1)-kC0
     =A n-A-dQ+k*(d-4)/(d+1)².
Substitutingk<=(n-1)/dandmultiplyingbydprovesthestatedbound.
