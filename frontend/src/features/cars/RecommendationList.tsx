import { ArrowUpRight, Fuel, Heart, Scale } from 'lucide-react'
import type { Recommendation } from '../../services/api/chats'

export function RecommendationList({ recommendations }: { recommendations: Recommendation[] }) {
  if (!recommendations.length) return null
  return <section className="recommendation-section"><div className="section-heading"><div><p className="section-kicker">Shortlist</p><h2>Three ways forward</h2></div><span className="count-badge">{recommendations.length} matches</span></div><div className="recommendation-grid">{recommendations.map((car, index) => <article className="recommendation-card" key={car.vehicle_id}><div className="card-topline"><span className="rank">0{index + 1}</span><button className="icon-button" aria-label={`Save ${car.vehicle_name}`}><Heart size={17} /></button></div><h3>{car.vehicle_name}</h3><p className="fit-summary">{car.fit_summary}</p><div className="price-line">{car.price_summary}</div><div className="tag-row">{car.match_reasons.slice(0, 2).map((reason) => <span className="tag" key={reason}><Fuel size={12} />{reason.replace('matches your ', '')}</span>)}</div><div className="card-actions"><button><Scale size={15} /> Compare</button><button><ArrowUpRight size={15} /> Details</button></div><div className="tradeoff"><strong>Watch for</strong><span>{car.considerations[0]}</span></div></article>)}</div></section>
}
