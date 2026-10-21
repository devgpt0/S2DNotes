# 3-Day Applied AI Workshop Curriculum
## Machine Learning, Deep Learning, and Generative AI

---

## 📅 Day 1 — NLP and LLM Fundamentals
**Structure:** 2 Hours Theory + 1 Hour Practical

### 📘 Theory (2 Hours)

| Time | Topic | Core Concepts to Cover |
| :--- | :--- | :--- |
| **25 min** | **NLP Fundamentals** | NLP definition, real-world use cases, text preprocessing, and tokenization. |
| **25 min** | **Text Representation** | Bag of Words (BoW) vs. TF-IDF vs. Embeddings; semantic similarity. |
| **35 min** | **Transformers & LLMs** | Attention intuition, Transformer architecture, BERT vs. GPT, and pretrained models. |
| **20 min** | **RAG Fundamentals** | Chunking, embeddings, vector retrieval, context injection, and answer generation. |
| **15 min** | **Prompt Engineering** | Instructions, context windows, forcing output formats, and managing hallucinations. |

### 💻 Practical Session (1 Hour)
* **Project:** Build a basic PDF question-answering chatbot.
* **10 min:** Load a PDF file and extract raw text data.
* **15 min:** Split text into chunks and generate vector embeddings.
* **20 min:** Retrieve relevant chunks and generate answers using a foundational model.
* **15 min:** Test with user queries and analyze/discuss incorrect or hallucinated answers.

🎯 **Pedagogical Priority:** Students must understand the end-to-end mechanics of an LLM-based application, focusing on pipeline architecture over simply writing text prompts.

---

## 📅 Day 2 — Computer Vision and CNNs
**Structure:** 2 Hours Theory + 1 Hour Practical

### 📘 Theory (2 Hours)

| Time | Topic | Core Concepts to Cover |
| :--- | :--- | :--- |
| **20 min** | **Image Fundamentals** | Pixels, image dimensions, coordinate systems, RGB channels, and grayscale. |
| **25 min** | **Image Preprocessing** | Resizing, filtering, thresholding, and edge detection techniques. |
| **40 min** | **CNN Fundamentals** | Convolution operations, filters/kernels, feature maps, pooling layers, and classification heads. |
| **20 min** | **Transfer Learning** | Leveraging pretrained models (ResNet/VGG), and feature extraction vs. fine-tuning. |
| **15 min** | **Evaluation Metrics** | Confusion matrix, accuracy, precision, recall, and F1-score. |

### 💻 Practical Session (1 Hour)
* **Project:** Build an image classification application using a pretrained CNN.
* **10 min:** Load sample image datasets and implement required preprocessing pipelines.
* **25 min:** Run inference on the images using a production-ready pretrained model.
* **15 min:** Extract and display predicted classes alongside their confidence scores.
* **10 min:** Evaluate incorrect predictions to diagnose and discuss model limitations.

🎯 **Pedagogical Priority:** Students should explicitly understand how a CNN extracts visual features hierarchically and how transfer learning reduces computational/training costs.

---

## 📅 Day 3 — Object Detection and AI Applications
**Structure:** 2 Hours Theory + 1 Hour Practical

### 📘 Theory (2 Hours)

| Time | Topic | Core Concepts to Cover |
| :--- | :--- | :--- |
| **30 min** | **Object Detection** | Image classification vs. object detection vs. segmentation; bounding boxes and Intersection over Union (IoU). |
| **25 min** | **YOLO (You Only Look Once)** | Single-shot real-time object detection mechanics and industry use cases. |
| **30 min** | **Multimodal AI** | Bridging text and image spaces; Optical Character Recognition (OCR) and image captioning. |
| **20 min** | **Deployment & Infrastructure** | Model inference bottlenecks, latency optimizations, memory constraints, APIs, and user interfaces. |
| **15 min** | **Responsible AI** | Addressing dataset bias, privacy concerns, downstream hallucinations, and ethical evaluation. |

### 💻 Practical Session (1 Hour)
* **Project:** Build a real-time object detection demo using a pretrained YOLO model.
* **10 min:** Load the YOLO weights and configure the tensor input specifications.
* **25 min:** Execute real-time object detection loops on static images or a video feed.
* **15 min:** Dynamically render bounding boxes, category labels, and confidence scores.
* **10 min:** Benchmark performance metrics and discuss accuracy vs. speed trade-offs.

🎯 **Pedagogical Priority:** Students must be able to explain the entire technical workflow from raw input arrays to downstream predictions, mapping technologies to their correct business use cases.

---

## ❌ Scope Boundaries (Deliberate Exclusions)
Given the **6-hour theoretical constraint**, the following complex topics are intentionally omitted from this short-form workshop:
* Mathematical proofs and inner derivations of recurrent architectures (RNNs, LSTMs, GRUs).
* Training multi-billion parameter Transformer models completely from scratch.
* Writing backpropagation algorithms or scratch CNN convolution loops in native arrays.
* Deep statistical physics/math behind Vision Transformers (ViTs) and Diffusion Models.
* Granular, standalone dives into traditional machine translation pipelines, generic NLP tasks, facial recognition matching algorithms, or pose estimation.

---

## 🎓 Core Learning Outcomes
By the conclusion of this 3-day course, students will be independently capable of:
1. **Architecting & Deploying RAG systems:** Design and build a functional document retrieval question-answering system hooked to an LLM.
2. **Implementing Computer Vision Inferences:** Successfully execute classification and real-time object detection utilizing industrial pretrained models.
3. **Evaluating System Trade-offs:** Articulate clear technical trade-offs involving vector embeddings, attention mechanisms, CNN features, transfer learning, statistical evaluation matrices, and runtime inference latencies.