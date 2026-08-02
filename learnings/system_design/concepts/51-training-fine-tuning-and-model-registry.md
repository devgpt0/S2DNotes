# Training, Fine-Tuning, and Model Registries

## Idea

Training changes model parameters using data. Fine-tuning adapts an existing model to a narrower task or domain.

A model registry records which exact model artifact was evaluated, approved, deployed, and rolled back.

## Visual model

```text
versioned data + code + configuration
                 |
           training workers
                 |
             checkpoints
                 |
          offline evaluation
                 |
            model registry
                 |
       canary -> production -> rollback
```

## Design steps

1. Start with prompting or retrieval and fine-tune only when evaluation shows a real gap.
2. Freeze a versioned training and evaluation dataset.
3. Record code, parameters, base model, tokenizer, libraries, and random seeds.
4. Write recoverable checkpoints during long training jobs.
5. Evaluate quality, safety, latency, and cost before registration.
6. Register the complete serving package, not only its weights.
7. Promote through explicit stages such as candidate, approved, and production.
8. Deploy gradually and retain a tested rollback artifact.

## Choosing an adaptation method

| Method | Best fit | Main cost |
|---|---|---|
| Prompting | Behavior can be expressed with instructions or examples | Larger prompts |
| Retrieval | Knowledge changes often or needs citations | Retrieval infrastructure |
| Parameter-efficient fine-tuning | Domain behavior must change with limited compute | Adapter lifecycle |
| Full fine-tuning | Deep behavior change with enough high-quality data | Highest compute and risk |

## Distributed training concerns

- Split data and model state only when one worker is insufficient.
- Checkpoint optimizer state as well as weights when training must resume exactly.
- Detect failed or slow workers instead of waiting forever.
- Make jobs restartable because large training runs will eventually fail.

## Common mistakes

- Fine-tuning to solve a retrieval or product-design problem.
- Selecting the model using the final test set.
- Losing the dataset and configuration that produced a model.
- Creating a training-serving preprocessing mismatch.
- Ignoring base-model licenses and data-use restrictions.
