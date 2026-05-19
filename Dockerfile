# 1. Base image ko update kiya (Node 20 use karne se naya Debian milega aur apt-get fail nahi hoga)
FROM nikolaik/python-nodejs:python3.10-nodejs20

# 2. System dependencies install karna
# Naye base image mein purani lists remove karne ki zaroorat nahi padegi
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg aria2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/

# 3. Pehle sirf requirements.txt copy karein (Caching Optimization)
# Isse baar-baar code change karne par pip install wapas se run nahi hoga aur build fast hoga
COPY requirements.txt .

# 4. Python packages install karna
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# 5. Ab baaki ka poora code copy karein
COPY . .

# 6. CMD ko JSON array format mein likha (tumhare pichle logs mein iski warning thi)
CMD ["bash", "start"]
