* Trade Project Preliminary Analysis Replication
* 2024 June 12
* By Siling Song

* Importing the file
clear
import delimited "/Users/LindaSong/Desktop/usa_00002.csv"
svyset cluster [pweight=perwt], strata(strata)
*describe

* filter out rows with NA values in any column
egen nmissing = rowmiss(*)
drop if nmissing > 0
drop nmissing

* filter out rows with INCWAGE as 999999 (indicating N/A) and 999998 (indicating Missing)
drop if incwage == 999999
drop if incwage == 999998

* filter out rows with IND 1990 showing unemployed (992) or N/A (0) or Does not Respond(999)
drop if ind1990 == 0
drop if ind1990 == 992
drop if ind1990 == 999

* creating a new variable ifsktrade:
* ifsktrad == 1 means this is a skilled trade
* ifsktrad == 0 means this is not a skilled trade
generate ifsktrad = 1 if (ind1990 >= 10 & ind1990 <= 32) | (ind1990 >= 40 & ind1990 <= 50)| ///
(ind1990 == 60)| (ind1990 >= 100 & ind1990 <= 392)| ///
(ind1990 >= 400 & ind1990 <= 472)|(ind1990 >= 751 & ind1990 <= 760)| (ind1990 >= 772 & ind1990 <= 780)| ///
(ind1990 == 832)
replace ifsktrad = 0 if ifsktrad == .
generate ifsktradwei = ifsktrad * perwt

* Calculate the sum of ifsktradwei and store it in a scalar trad
summarize ifsktradwei
scalar trad = r(sum)

* Calculate the sum of perwt and store it in a scalar total
summarize perwt
scalar total = r(sum)

* Calculate the percentage
scalar pct = trad / total
summarize ifsktrad
display pct

svy: tabulate ifsktrad

* Sex breakdown for trade
*preserve

*keep if ifsktrad == 1
*svy: tabulate sex
*tabulate sex

*svy: tabulate age
*svy: tabulate race
*svy: tabulate hispan
*svy: tabulate region
*svy: tabulate marst
*svy: tabulate educ
*svy: tabulate educd
*svy: tabulate uhrswork
*svy: tabulate looking
*svy: mean incwage


*restore


*labeling the data for some of the variables:
label define educd_labels ///
    002 "No schooling completed" ///
    010 "Nursery school to grade 4" ///
    011 "Nursery school, preschool" ///
    012 "Kindergarten" ///
    013 "Grade 1, 2, 3, or 4" ///
    014 "Grade 1" ///
    015 "Grade 2" ///
    016 "Grade 3" ///
    017 "Grade 4" ///
    020 "Grade 5, 6, 7, or 8" ///
    021 "Grade 5 or 6" ///
    022 "Grade 5" ///
    023 "Grade 6" ///
    024 "Grade 7 or 8" ///
    025 "Grade 7" ///
    026 "Grade 8" ///
    030 "Grade 9" ///
    040 "Grade 10" ///
    050 "Grade 11" ///
    060 "Grade 12" ///
    061 "12th grade, no diploma" ///
    062 "High school graduate or GED" ///
    063 "Regular high school diploma" ///
    064 "GED or alternative credential" ///
    065 "Some college, but less than 1 year" ///
    070 "1 year of college" ///
    071 "1 or more years of college credit, no degree" ///
    080 "2 years of college" ///
    081 "Associate's degree, type not specified" ///
    082 "Associate's degree, occupational program" ///
    083 "Associate's degree, academic program" ///
    090 "3 years of college" ///
    100 "4 years of college" ///
    101 "Bachelor's degree" ///
    110 "5+ years of college" ///
    111 "6 years of college (6+ in 1960-1970)" ///
    112 "7 years of college" ///
    113 "8+ years of college" ///
    114 "Master's degree" ///
    115 "Professional degree beyond a bachelor's degree" ///
    116 "Doctoral degree"

* Apply labels to the educd variable
label values educd educd_labels

*  Define labels for region variable
label define region_labels ///
    11 "New England Division" ///
    12 "Middle Atlantic Division" ///
    13 "Mixed Northeast Divisions" ///
    21 "East North Central Division" ///
    22 "West North Central Division" ///
    23 "Mixed Midwestern Divisions" ///
    31 "South Atlantic Division" ///
    32 "East South Central Division" ///
    33 "West South Central Division" ///
    34 "Mixed Southern Divisions" ///
    41 "Mountain Division" ///
    42 "Pacific Division" ///
    43 "Mixed Western Divisions" ///
    91 "Overseas Military/Military Installations" ///
    92 "PUMA boundaries cross state lines - Metro sample" ///
    97 "State not identified" ///
    99 "Not identified"

* Apply labels to the region variable
label values region region_labels

* Step 1: Define labels for race variable
label define race_labels ///
    1 "White" ///
    2 "Black/African American" ///
    3 "American Indian or Alaska Native" ///
    4 "Chinese" ///
    5 "Japanese" ///
    6 "Other Asian or Pacific Islander" ///
    7 "Other race, nec" ///
    8 "Two major races" ///
    9 "Three or more major races"

* Step 2: Apply labels to the race variable
label values race race_labels

* Step 1: Define labels for hispan variable
label define hispan_labels ///
    0 "Not Hispanic" ///
    1 "Mexican" ///
    2 "Puerto Rican" ///
    3 "Cuban" ///
    4 "Other" ///
    9 "Not Reported"

* Step 2: Apply labels to the hispan variable
label values hispan hispan_labels


* Step 1: Define labels for marst variable
label define marst_labels ///
    1 "Married, spouse present" ///
    2 "Married, spouse absent" ///
    3 "Separated" ///
    4 "Divorced" ///
    5 "Widowed" ///
    6 "Never married/single" ///
    9 "Blank, missing"

* Step 2: Apply labels to the marst variable
label values marst marst_labels

label define sex_labels ///
    1 "Male" ///
    2 "Female" ///
    9 "Blank, missing"

* Step 2: Apply labels to the marst variable
label values sex sex_labels

* Step 1: Define labels for looking variable
label define looking_labels ///
    0 "N/A" ///
    1 "No, did not look for work" ///
    2 "Yes, looked for work" ///
    3 "Not reported"

* Step 2: Apply labels to the looking variable
label values looking looking_labels

* Running discrete models:

* linear probability model: 
* svy: regress ifsktrad ib63.educd age i.sex i.race i.hispan i.region i.marst  i.looking

* probit model: 
* svy: probit ifsktrad ib63.educd age i.sex i.race i.hispan i.region i.marst  i.looking

* logit model:
* svy: logit ifsktrad ib63.educd age i.sex i.race i.hispan i.region i.marst i.looking

* determining whether being in a skilled trade industry increases income:

svy: regress incwage  i.ifsktrad  ib63.educd  i.sex i.race i.hispan i.region i.marst i.looking

