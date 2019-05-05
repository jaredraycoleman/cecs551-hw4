# CECS 551 - HW 4

## Usage

To train, run:
```bash
python fine_tune_code.py <path/to/data> --out <path/to/save/model.h5>
```

To test on a single image, run:
```bash
python test_model.py <path/to/model.h5> <path/to/image.jpg>
```

## Homework Questions
**Q1:** I attained a *validation* accuracy of 49.86%. This makes sense since we have two classes are are barely training. Essentially, the model is simply guessing between *cat* and *dog*.

**Q2:** 