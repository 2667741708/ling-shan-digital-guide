<template>
  <main class="home page">
    <nav class="top-nav">
      <strong>LingTour AI 数字人导游平台</strong>
      <router-link to="/admin">管理后台</router-link>
    </nav>
    <section class="hero">
      <div>
        <h1>灵境导游</h1>
        <p>语音问答、路线推荐、景点讲解和游客感受度分析的一体化景区数字人系统。</p>
        <div class="actions">
          <router-link class="primary" to="/guide">进入数字人导览</router-link>
          <router-link to="/map">查看景区地图</router-link>
        </div>
      </div>
    </section>
  </main>
</template>
