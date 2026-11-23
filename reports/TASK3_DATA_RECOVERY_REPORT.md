# TASK 3 - Data Recovery Report

**Recovery date:** 2026-11-21

## Recovery status

The real Kaggle and O*NET datasets were restored byte-for-byte from the independent source directory `C:\Users\Asus\Desktop\data-dl`. Each destination hash matched its source. The independent source directory was not modified.

## Kaggle recovery

- **Source archive:** `C:\Users\Asus\Desktop\data-dl\kaggle\archive (4).zip`
- **Archive SHA-256:** `B12C4AB34DF707AD2CC64312C016509CAD9B6C93B0BAED7A6A2C7CBD6B2B7AA4`
- **Source member:** `Resume/Resume.csv`
- **Destination:** `data/raw/kaggle/extracted/Resume/Resume.csv`
- **Destination SHA-256:** `816A7CD985A9A41E3CE8D1E83CB7E1BEB1E854A89C1CF1FD0D75494FAAA0559`
- **Byte comparison:** PASS; ZIP member and destination bytes are identical.
- **Dimensions:** 2,484 rows x 4 columns
- **Schema:** `ID`, `Resume_str`, `Resume_html`, `Category`
- **Categories:** 24
- **Missing values:** none
- **Duplicate IDs:** 0
- **Duplicate rows:** 0

## O*NET recovery

| File | Source | Destination | Dimensions | Schema | Missing cells | Duplicate rows | Source/destination SHA-256 |
|---|---|---|---:|---|---:|---:|---|
| occupation_data.csv | `C:\Users\Asus\Desktop\data-dl\onet\occupation_data.csv` | `data/raw/onet/occupation_data.csv` | 1,016 x 3 | `O*NET-SOC Code`, `Title`, `Description` | 0 | 0 | `A09EAE1D6609686E44E05B7290993A1C8B523D8CA224BC0EEDC194C855C3EE02` |
| software_skills.csv | `C:\Users\Asus\Desktop\data-dl\onet\software_skills.csv` | `data/raw/onet/software_skills.csv` | 31,821 x 7 | `O*NET-SOC Code`, `Title`, `Workplace Example`, `Element ID`, `Element Name`, `Hot Technology`, `In Demand` | 0 | 0 | `6AABB96B464288DB849580E6510530EFFF3F80E25DDE2BB23F1FC36BB526B016` |
| essential_skills.csv | `C:\Users\Asus\Desktop\data-dl\onet\essential_skills.csv` | `data/raw/onet/essential_skills.csv` | 18,200 x 15 | `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Data Value`, `N`, `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Not Relevant`, `Date`, `Domain Source` | 9,100 | 0 | `68C4D31D8C55077238395DCA40CC4E6D32E6A608B5474BB8264B1F98AE415BD7` |
| task_statements.csv | `C:\Users\Asus\Desktop\data-dl\onet\task_statements.csv` | `data/raw/onet/task_statements.csv` | 18,838 x 8 | `O*NET-SOC Code`, `Title`, `Task ID`, `Task`, `Task Type`, `Incumbents Responding`, `Date`, `Domain Source` | 1,005 | 0 | `4568E14D8DB6F05551AD37E056E909B13EBAE4A26BCB5FF915BB5F281D582C57` |

The O*NET source files contain 69,875 records in total.

## Backup of replaced synthetic artifacts

The previous synthetic destination files were copied before replacement to `reports/backups/synthetic_raw/`.

| Original destination | Backup | Original SHA-256 |
|---|---|---|
| `data/raw/kaggle/extracted/Resume/Resume.csv` | `reports/backups/synthetic_raw/Resume.csv` | `D8242DD0A28704F5BEA8320A8C5FFCD9ED01FC12E364B982F98D83C0A885F52C` |
| `data/raw/onet/occupation_data.csv` | `reports/backups/synthetic_raw/occupation_data.csv` | `994DD444FA090FC5B0043562BB571B4EC15555AEE6D5931E60867C16515B9391` |
| `data/raw/onet/software_skills.csv` | `reports/backups/synthetic_raw/software_skills.csv` | `C1968BC5ECB261A874CDB12632DF1A5EA263948A19D83B6C29926697E82622D3` |
| `data/raw/onet/essential_skills.csv` | `reports/backups/synthetic_raw/essential_skills.csv` | `73BFC6232EB5CABDE65743BF8AABC7B2FAC9F22EF65CF0F0D1FF535C6D8E3556` |
| `data/raw/onet/task_statements.csv` | `reports/backups/synthetic_raw/task_statements.csv` | `784DBE58E0915A717427164DD03B2548D9F6AFEE9ACACB08E52FAE8B6D9D92B4` |

## Validation result

- Kaggle archive member exists and is readable.
- Kaggle schema, dimensions, categories, and duplicate/blank checks match expectations.
- All O*NET schemas match the source definitions.
- All O*NET source/destination hashes match.
- Cross-file SOC code consistency and detailed data-quality checks remain to be executed in the validation stage.
